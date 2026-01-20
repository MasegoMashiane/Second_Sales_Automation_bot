from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path
import csv
import json
import subprocess
import psutil
import os 
import signal
from datetime import datetime
from datetime import timedelta
from werkzeug.utils import secure_filename

sys.path.insert(0, str(Path(__file__).parent.parent))
from Config import Config
from src.database.sheets_manager import SheetsManager


app = Flask(__name__)
CORS(app)

#Upload configuration 
UPLOAD_FOLDER = Path(__file__).parent.parent / 'data' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webp'}

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit

#global state
bot_process = None
sheets_manager = None

def init_manager():
    #Initialize managers
    global sheets_manager
    if sheets_manager is None:
        try:
            sheets_manager = SheetsManager()
        except Exception as e:
            print(f"Warning: Could not initialize SheetsManager: {e}")
            return False
    return True

def allowed_file(filename):
    #Chceck if the file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            


# HEALTH AND STATUS ENDPOINTS

@app.route('/health', methods=['GET'])
def health_check():
    # health check endpoint
    return jsonify({
        'status': 'Healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'api': 'running',
            'sheets': 'connected' if sheets_manager else 'disconnected', 
            'bot': 'running' if check_bot_running() else 'stopped'
        }
    })           

@app.route('/api/status', methods=['GET'])
def get_status():
    #get bot status
    is_running = check_bot_running()
    uptime = get_uptime() if is_running else 0

    return jsonify({
        'status': 'running' if is_running else 'stopped',
        'last_sync': datetime.now().isoformat(),
        'uptime': uptime,
        'uptime_formatted': format_uptime(uptime)
    })


#DASHBOARD ENDPOINTS

@app.route('/api/quotas', methods=['GET'])
def get_quotas():
    #Get quota usage for all platforms
    activity = analyze_activity_log()

    return jsonify({
        'email':{
            'used': activity['Email']['Success'] + activity['Email']['Failed'],
            'limit': Config.EMAIL_DAILY_LIMIT,
            'success': activity['Email']['Success'],
            'failed': activity['Email']['Failed']
        },
        'facebook':{
            'used': activity['Facebook']['Success'] + activity['Facebook']['Failed'],
            'limit': Config.FACEBOOK_DAILY_LIMIT,
            'success': activity['Facebook']['Success'],
            'failed': activity['Facebook']['Failed']
        },
        'Instagram':{
          'used': activity['Instagram']['Success'] + activity['Instagram']['Failed'],
          'limit': Config.INSTAGRAM_DAILY_LIMIT,
          'success': activity['Instagram']['Success'],
          'failed': activity['Instagram']['Failed']
        }
    })

@app.route('/api/activity/recent', methods=['GET'])
def get_recent_activity():
    limit = request.args.get('limit', 50, type=int)

    log_file = Config.ACTIVITY_LOG
    if not log_file.exists():
        return jsonify([])
    
    activities = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            #Get last N activities
            for row in reversed(rows[-limit:]):
                try:
                    timestamp = datetime.fromisoformat(row['Timestamp'])
                    activities.append({
                        'time': timestamp.strftime('%I:%M %p'),
                        'datetime': timestamp.isoformat(),
                        'type': row['Type'],
                        'status': row['Status'],
                        'details': row['Details']
                    })
                except:
                    continue
    except Exception as e:
        print(f"Error reading activity log: {e}")
    
    return jsonify(activities)

@app.route('/api/stats/weekly', methods=['GET'])
def get_weekly_stats():
    stats = []
    today = datetime.now()

    for i in range(7):
        day = today - timedelta(days=6-i)
        day_stats = get_day_stats(day)
        stats.append({
            'day': day.strftime('%a'),
            'data': day.strftime('%Y-%m-%d'),
            'emails':day_stats['emails'],
            'posts': day_stats['posts']
        })
    return jsonify(stats)

@app.route('/api/engagement', methods=['GET'])
def get_engagement():
    #In production, fetch from platform APIs
    #Returns mock data for now
    return jsonify([{'platform': 'Facebook', 'Likes': 120, 'comments': 45, 'shares': 23},
                    {'platform': 'Instagram', 'Likes': 350, 'comments': 89, 'shares': 67}])


#Social Media Post Endpoints

@app.route('/api/posts', methods=['GET'])
def get_scheduled_posts():
    if not init_manager():
        return jsonify({'error': 'sheets manager not initialized'}), 500
    
    try:
        posts = sheets_manager.get_social_post()

        formatted_posts = []
        for idx, post in enumerate(posts):
            formatted_posts.append({
                'id': idx + 1,
                'platform': post.get('Platform', ''),
                'caption': post.get('Text', ''),
                'hashtags': post.get('Hashtags', ''),
                'date': post.get('Date', ''),
                'time': post.get('Time', ''),
                'status': post.get('Status', 'Pending'),
                'media': post.get('Media', None),
                'posted_time': post.get('Posted Time', ''),
                'post_id': post.get('Post ID', '')
            })

        return jsonify(formatted_posts)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/posts', methods=['POST'])
def create_scheduled_post():
    if not init_manager():
        return jsonify ({'error': 'Sheets manager not initialized'}), 500
    
    try:
        #get form data
        platform = request.form.get('platform')
        caption = request.form.get('caption')
        hashtags = request.form.get('hashtags', '')
        scheduled_date = request.form.get('scheduleDate')
        scheduled_time = request.form.get('scheduleTime')

        #handle file upload
        media_filename = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #add timestamp to filneame to avoid conflict
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                media_filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], media_filename)
                file.save(file_path)

                #validate require fields
                if not all ([platform, caption, scheduled_date, scheduled_time]):
                    return jsonify({'error': 'Missing required fields'}), 400
                
                #Instagram requires media
                if platform == 'Instagram' and not media_filename:
                    return jsonify({'error': 'Instagram requires an image or video'}), 400
                
                #Add to google sheets
                sheet = sheets_manager.client.open(Config.SOCIAL_SHEET_NAME).sheet1

                # Prepare row data
                new_row = [
                    scheduled_date,
                    scheduled_time,
                    platform,
                    caption,
                    media_filename or '',
                    hashtags,
                    'Pending',
                    '', 
                    ''
                ]

                #Append to sheet 
                sheet.append_row(new_row)

                return jsonify({
                    'success': True,
                    'message': 'Post scheduled successfully',
                    'data': {
                        'platform': platform,
                        'caption': caption,
                        'date': scheduled_date,
                        'time': scheduled_time,
                        'media': media_filename
                        }
                    }), 201
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_scheduled_post(post_id):
    if not init_manager():
        return jsonify({'error': 'Sheets manager not initialized'}), 500
    
    try:
        sheet= sheets_manager.client.open(Config.SOCIAL_SHEET_NAME).sheet1

        #Delete row
        row_num = post_id + 1
        sheet.delete_rows(row_num)

        return jsonify({
            'success': True,
            'message': 'Post succesfully deleted'
        })


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_scheduled_post(post_id):
    if not init_manager():
        return jsonify({'error': 'Sheets manager not initialized'}), 500

    try:
        data = request.get_json()
        sheet = sheets_manager.client.open(Config.SOCIAL_SHEET_NAME).sheet1
        
        row_num = post_id + 1
        
        if 'caption' in data:
            sheet.update_cell(row_num, 4, data['caption'])
        if 'hashtags' in data:
            sheet.update_cell(row_num, 6, data['hashtags'])
        if 'scheduleDate' in data:
            sheet.update_cell(row_num, 1, data['scheduleDate'])
        if 'scheduleTime' in data:
            sheet.update_cell(row_num, 2, data['scheduleTime'])
        
        return jsonify({
            'success': True,
            'message': 'Post updated successfully'
            })


    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#File upload endpoints

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload media file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        media_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], media_filename)
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        return jsonify({
            'success': True,
            'filename': media_filename,
            'url': f'/api/uploads/{media_filename}',
            'size': file_size
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Campaing endpoints


@app.route('/api/campaigns/sales', methods=['GET'])
def get_sales_campaigns():
    """Get sales campaign status"""
    if not init_manager():
        return jsonify({'campaigns': []})
    
    try:
        leads = sheets_manager.get_sales_leads()
        
        stage_counts = {0: 0, 1: 0, 2: 0}
        for lead in leads:
            stage = int(lead.get('Stage', 0))
            if stage in stage_counts:
                stage_counts[stage] += 1
        
        return jsonify({
            'campaigns': [
                {
                    'name': 'Initial Outreach Campaign',
                    'stage': 'Stage 0 - New Leads',
                    'count': stage_counts[0],
                    'description': 'First contact with new prospects'
                },
                {
                    'name': 'Follow-up Campaign 1',
                    'stage': 'Stage 1 - 3 Days After',
                    'count': stage_counts[1],
                    'description': 'First follow-up after 3 days'
                },
                {
                    'name': 'Follow-up Campaign 2',
                    'stage': 'Stage 2 - 7 Days After',
                    'count': stage_counts[2],
                    'description': 'Final follow-up after 7 days'
                }
            ],
            'total_leads': len(leads)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'campaigns': []}), 500

@app.route('/api/campaigns/social', methods=['GET'])
def get_social_schedule():
    """Get upcoming scheduled social media posts"""
    if not init_manager():
        return jsonify([])
    
    try:
        posts = sheets_manager.get_social_post()
        
        upcoming = []
        for post in posts:
            if post.get('Status') == 'Pending':
                try:
                    post_time = datetime.strptime(
                        f"{post['Date']} {post['Time']}", 
                        "%Y-%m-%d %H:%M"
                    )
                    if post_time > datetime.now():
                        upcoming.append({
                            'platform': post['Platform'],
                            'text': post['Text'][:50] + '...' if len(post['Text']) > 50 else post['Text'],
                            'scheduled': post_time.strftime('%b %d, %I:%M %p'),
                            'datetime': post_time.isoformat()
                        })
                except:
                    continue
        
        # Sort by datetime
        upcoming.sort(key=lambda x: x['datetime'])
        
        return jsonify(upcoming[:10])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Bot Control Endpoints


@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the automation bot"""
    global bot_process
    
    if check_bot_running():
        return jsonify({'error': 'Bot is already running'}), 400
    
    try:
        # Start bot process
        python_path = sys.executable
        script_path = Path(__file__).parent.parent / 'run_scheduler.py'
        
        bot_process = subprocess.Popen(
            [python_path, str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(script_path.parent)
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Bot started successfully',
            'pid': bot_process.pid
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the automation bot"""
    global bot_process
    
    if not check_bot_running():
        return jsonify({'error': 'Bot is not running'}), 400
    
    try:
        # Kill bot processes
        killed = kill_bot_processes()
        
        if bot_process:
            try:
                bot_process.terminate()
                bot_process.wait(timeout=5)
            except:
                bot_process.kill()
        
        return jsonify({
            'status': 'success',
            'message': f'Bot stopped successfully (killed {killed} processes)'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bot/restart', methods=['POST'])
def restart_bot():
    """Restart the automation bot"""
    try:
        # Stop if running
        if check_bot_running():
            stop_bot()
            import time
            time.sleep(2)
        
        # Start
        return start_bot()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Utility Endpoitns

@app.route('/api/backup', methods=['POST'])
def trigger_backup():
    """Trigger data backup"""
    try:
        script_path = Path(__file__).parent.parent / 'scripts' / 'backup_data.py'
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(script_path.parent.parent)
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Backup completed',
            'output': result.stdout,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-connections', methods=['POST'])
def test_connections():
    """Test API connections"""
    try:
        script_path = Path(__file__).parent.parent / 'scripts' / 'test_connections.py'
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(script_path.parent.parent)
        )
        
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr if result.stderr else None
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Connection test timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get recent logs"""
    lines = request.args.get('lines', 100, type=int)
    log_type = request.args.get('type', 'main')  # main or activity
    
    if log_type == 'activity':
        log_file = Config.ACTIVITY_LOG
    else:
        log_file = Config.LOG_FILE
    
    if not log_file.exists():
        return jsonify({'logs': []})
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
            return jsonify({'logs': log_lines[-lines:]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# HELPER FUNCTIONS
# ============================================

def check_bot_running():
    """Check if bot process is running"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'run_scheduler.py' in ' '.join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def kill_bot_processes():
    """Kill all bot processes"""
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'run_scheduler.py' in ' '.join(cmdline):
                proc.terminate()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed

def get_uptime():
    """Get bot uptime in seconds"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'run_scheduler.py' in ' '.join(cmdline):
                return int(datetime.now().timestamp() - proc.info['create_time'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return 0

def format_uptime(seconds):
    """Format uptime in human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def analyze_activity_log():
    """Analyze activity log for last 24 hours"""
    log_file = Config.ACTIVITY_LOG
    
    if not log_file.exists():
        return {
            'Email': {'Success': 0, 'Failed': 0},
            'Facebook': {'Success': 0, 'Failed': 0},
            'Instagram': {'Success': 0, 'Failed': 0},
            'LinkedIn': {'Success': 0, 'Failed': 0}
        }
    
    cutoff_time = datetime.now() - timedelta(hours=24)
    counts = {
        'Email': {'Success': 0, 'Failed': 0},
        'Facebook': {'Success': 0, 'Failed': 0},
        'Instagram': {'Success': 0, 'Failed': 0},
        'LinkedIn': {'Success': 0, 'Failed': 0}
    }
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row['Timestamp'])
                    if timestamp > cutoff_time:
                        activity_type = row['Type']
                        status = row['Status']
                        if activity_type in counts:
                            counts[activity_type][status] = counts[activity_type].get(status, 0) + 1
                except:
                    continue
    except Exception as e:
        print(f"Error analyzing activity log: {e}")
    
    return counts

def get_day_stats(date):
    """Get statistics for a specific day"""
    log_file = Config.ACTIVITY_LOG
    
    if not log_file.exists():
        return {'emails': 0, 'posts': 0}
    
    day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    
    stats = {'emails': 0, 'posts': 0}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row['Timestamp'])
                    if day_start <= timestamp < day_end and row['Status'] == 'Success':
                        if row['Type'] == 'Email':
                            stats['emails'] += 1
                        elif row['Type'] in ['Facebook', 'Instagram', 'LinkedIn']:
                            stats['posts'] += 1
                except:
                    continue
    except Exception as e:
        print(f"Error getting day stats: {e}")
    
    return stats

#error handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

# SHUTDOWN HANDLER

def shutdown_handler(signum, frame):
    """Handle shutdown gracefully"""
    print("\nShutting down API server...")
    
    # Kill bot processes
    if bot_process:
        bot_process.terminate()
    
    kill_bot_processes()
    
    sys.exit(0)

# Register shutdown handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


#run Server
if __name__ == '__main__':
    print("=" * 60)
    print("Sales Automation API Server")
    print("=" * 60)
    print(f"Dashboard URL: http://localhost:5000")
    print(f"API Endpoints: http://localhost:5000/api/")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Environment: {'Development' if app.debug else 'Production'}")
    print("=" * 60)
    print("\nAvailable Endpoints:")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/status              - Bot status")
    print("  GET  /api/quotas              - API quota usage")
    print("  GET  /api/activity/recent     - Recent activity")
    print("  GET  /api/posts               - Scheduled posts")
    print("  POST /api/posts               - Create post")
    print("  POST /api/bot/start           - Start bot")
    print("  POST /api/bot/stop            - Stop bot")
    print("=" * 60)
    print("\nPress Ctrl+C to stop\n")
    
    # Create necessary directories
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Initialize sheets manager
    init_manager()
    
    print("FLASK_API_READY", flush=True)
    # Run server
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000, threaded=True)