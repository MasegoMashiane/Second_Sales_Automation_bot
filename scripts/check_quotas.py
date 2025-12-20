import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from Config import Config
from src.utils.logger import logger
import csv

def analyze_activity_log():
    #Analyze recent activity from log
    log_file = Config.ACTIVITY_LOG
    
    if not log_file.exists():
        print("No activity log found")
        return {}
    
    # Count activities in last 24 hours
    cutoff_time = datetime.now() - timedelta(hours=24)
    counts = {
        'Email': {'Success': 0, 'Failed': 0},
        'Facebook': {'Success': 0, 'Failed': 0},
        'Instagram': {'Success': 0, 'Failed': 0}
    }
    
    with open(log_file, 'r') as f:
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
    
    return counts

def print_quota_report():
    #Print quota usage report
    print("=" * 60)
    print("API QUOTA USAGE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    counts = analyze_activity_log()
    
    # Email
    print("\\n📧 EMAIL (Gmail)")
    print("-" * 60)
    email_used = counts['Email']['Success'] + counts['Email']['Failed']
    email_limit = Config.EMAIL_DAILY_LIMIT
    email_pct = (email_used / email_limit * 100) if email_limit > 0 else 0
    print(f"Used: {email_used}/{email_limit} ({email_pct:.1f}%)")
    print(f"Success: {counts['Email']['Success']}")
    print(f"Failed: {counts['Email']['Failed']}")
    if email_pct > 80:
        print("⚠️  WARNING: Approaching daily limit!")
    
    # Facebook
    print("\\n📘 FACEBOOK")
    print("-" * 60)
    fb_used = counts['Facebook']['Success'] + counts['Facebook']['Failed']
    fb_limit = Config.FACEBOOK_DAILY_LIMIT
    fb_pct = (fb_used / fb_limit * 100) if fb_limit > 0 else 0
    print(f"Used: {fb_used}/{fb_limit} ({fb_pct:.1f}%)")
    print(f"Success: {counts['Facebook']['Success']}")
    print(f"Failed: {counts['Facebook']['Failed']}")
    if fb_pct > 80:
        print("⚠️  WARNING: Approaching daily limit!")
    
    # Instagram
    print("\\n📷 INSTAGRAM")
    print("-" * 60)
    ig_used = counts['Instagram']['Success'] + counts['Instagram']['Failed']
    ig_limit = Config.INSTAGRAM_DAILY_LIMIT
    ig_pct = (ig_used / ig_limit * 100) if ig_limit > 0 else 0
    print(f"Used: {ig_used}/{ig_limit} ({ig_pct:.1f}%)")
    print(f"Success: {counts['Instagram']['Success']}")
    print(f"Failed: {counts['Instagram']['Failed']}")
    if ig_pct > 80:
        print("⚠️  WARNING: Approaching daily limit!")
    
    # Summary
    print("\\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_success = sum(counts[k]['Success'] for k in counts)
    total_failed = sum(counts[k]['Failed'] for k in counts)
    total_operations = total_success + total_failed
    success_rate = (total_success / total_operations * 100) if total_operations > 0 else 0
    
    print(f"Total Operations: {total_operations}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate < 95:
        print("\\n⚠️  WARNING: Success rate below 95%! Investigate failures.")

if __name__ == "__main__":
    print_quota_report()