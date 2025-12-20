import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.sheets_manager import SheetsManager
from Config import Config

def backup_sheets():
    #Backup all Google Sheets to JSON files
    print("Starting backup...")
    
    # Create backup directory
    backup_dir = Config.DATA_DIR / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        sheets = SheetsManager()
        
        # Backup sales leads
        print("\\nBacking up sales leads...")
        leads = sheets.get_sales_leads()
        leads_file = backup_dir / f'sales_leads_{timestamp}.json'
        with open(leads_file, 'w') as f:
            json.dump(leads, f, indent=2)
        print(f"✓ Saved {len(leads)} leads to {leads_file}")
        
        # Backup social posts
        print("\\nBacking up social posts...")
        posts = sheets.get_social_posts()
        posts_file = backup_dir / f'social_posts_{timestamp}.json'
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)
        print(f"✓ Saved {len(posts)} posts to {posts_file}")
        
        # Create latest symlinks
        latest_leads = backup_dir / 'sales_leads_latest.json'
        latest_posts = backup_dir / 'social_posts_latest.json'
        
        if latest_leads.exists():
            latest_leads.unlink()
        if latest_posts.exists():
            latest_posts.unlink()
        
        latest_leads.symlink_to(leads_file.name)
        latest_posts.symlink_to(posts_file.name)
        
        print("\\n✓ Backup completed successfully!")
        print(f"\\nBackup location: {backup_dir}")
        
        # Clean old backups (keep last 30 days)
        print("\\nCleaning old backups...")
        cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        removed_count = 0
        
        for backup_file in backup_dir.glob('*.json'):
            if backup_file.name.endswith('_latest.json'):
                continue
            if backup_file.stat().st_mtime < cutoff_date:
                backup_file.unlink()
                removed_count += 1
        
        if removed_count > 0:
            print(f"✓ Removed {removed_count} old backup(s)")
        
    except Exception as e:
        print(f"\\n✗ Backup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    backup_sheets()