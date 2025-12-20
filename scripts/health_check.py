
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from Config import Config
from src.database.sheets_manager import SheetsManager
from src.email.email_client import EmailClient
from src.social.facebook_client import FacebookClient
from src.social.instagram_client import InstagramClient

class HealthChecker:
    #System health checker
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }
    
    def check_google_sheets(self):
        #Check Google Sheets connectivity
        try:
            sheets = SheetsManager()
            leads = sheets.get_sales_leads()
            self.results['checks']['google_sheets'] = {
                'status': 'healthy',
                'leads_count': len(leads)
            }
            return True
        except Exception as e:
            self.results['checks']['google_sheets'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            self.results['overall_status'] = 'unhealthy'
            return False
    
    def check_logs(self):
        #Check log files
        try:
            log_file = Config.LOG_FILE
            activity_log = Config.ACTIVITY_LOG
            
            # Check if logs exist and are recent
            log_age = None
            if log_file.exists():
                log_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                log_age = (datetime.now() - log_mtime).total_seconds() / 3600
            
            log_size = log_file.stat().st_size if log_file.exists() else 0
            activity_size = activity_log.stat().st_size if activity_log.exists() else 0
            
            status = 'healthy'
            if not log_file.exists() or not activity_log.exists():
                status = 'warning'
            elif log_age and log_age > 24:
                status = 'warning'
            
            self.results['checks']['logs'] = {
                'status': status,
                'log_size_mb': round(log_size / 1024 / 1024, 2),
                'activity_log_size_mb': round(activity_size / 1024 / 1024, 2),
                'log_age_hours': round(log_age, 1) if log_age else None
            }
            
            return status == 'healthy'
        except Exception as e:
            self.results['checks']['logs'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            return False
    
    def check_disk_space(self):
        #Check available disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (2**30)
            free_pct = (free / total) * 100
            
            status = 'healthy'
            if free_pct < 10:
                status = 'critical'
                self.results['overall_status'] = 'unhealthy'
            elif free_pct < 20:
                status = 'warning'
            
            self.results['checks']['disk_space'] = {
                'status': status,
                'free_gb': free_gb,
                'free_percent': round(free_pct, 1)
            }
            
            return status != 'critical'
        except Exception as e:
            self.results['checks']['disk_space'] = {
                'status': 'unknown',
                'error': str(e)
            }
            return True
    
    def check_api_configs(self):
        
        # Check API configurations
        configs = {
            'email': bool(Config.EMAIL_ADDRESS and Config.EMAIL_PASSWORD),
            'google_sheets': bool(Config.GOOGLE_SHEETS_CREDENTIALS),
            'facebook': bool(Config.META_ACCESS_TOKEN and Config.FACEBOOK_PAGE_ID),
            'instagram': bool(Config.META_ACCESS_TOKEN and Config.INSTAGRAM_ACCOUNT_ID),
        }
        
        configured_count = sum(configs.values())
        
        self.results['checks']['api_configs'] = {
            'status': 'healthy' if configured_count >= 2 else 'warning',
            'configured': configs,
            'configured_count': configured_count
        }
        
        return configured_count >= 2
    
    def run_all_checks(self):
        #Run all health checks
        print("=" * 60)
        print("SYSTEM HEALTH CHECK")
        print(f"Time: {self.results['timestamp']}")
        print("=" * 60)
        
        checks = [
            ("Google Sheets", self.check_google_sheets),
            ("Log Files", self.check_logs),
            ("Disk Space", self.check_disk_space),
            ("API Configs", self.check_api_configs)
        ]
        
        for name, check_func in checks:
            print(f"\\nChecking {name}...", end=" ")
            try:
                result = check_func()
                status = self.results['checks'][name.lower().replace(' ', '_')]['status']
                
                if status == 'healthy':
                    print("✓ HEALTHY")
                elif status == 'warning':
                    print("⚠ WARNING")
                else:
                    print("✗ UNHEALTHY")
            except Exception as e:
                print(f"✗ ERROR: {e}")
                self.results['overall_status'] = 'unhealthy'
        
        print("\\n" + "=" * 60)
        print(f"OVERALL STATUS: {self.results['overall_status'].upper()}")
        print("=" * 60)
        
        # Print detailed results
        print("\\nDetailed Results:")
        print(json.dumps(self.results, indent=2))
        
        # Save results
        health_file = Config.DATA_DIR / 'health_check.json'
        with open(health_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return self.results['overall_status'] == 'healthy'

def main():
    #Run health check
    checker = HealthChecker()
    is_healthy = checker.run_all_checks()
    
    sys.exit(0 if is_healthy else 1)

if __name__ == "__main__":
    main()