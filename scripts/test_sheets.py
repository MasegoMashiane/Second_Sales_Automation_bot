import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

project_root = Path(__file__).parent.parent
creds_path = project_root / 'Config' / 'credentials.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(
    str(creds_path), scope
)

client = gspread.authorize(creds)

# Test Sales Leads
try:
    sales_sheet = client.open('Sales Leads').sheet1
    data = sales_sheet.get_all_records()
    print(f"✓ Sales Leads: Found {len(data)} leads")
    print(f"  Columns: {list(data[0].keys()) if data else 'No data'}")
except Exception as e:
    print(f"✗ Sales Leads Error: {e}")

# Test Social Media Content
try:
    social_sheet = client.open('Social Media Content').sheet1
    data = social_sheet.get_all_records()
    print(f"✓ Social Media Content: Found {len(data)} posts")
    print(f"  Columns: {list(data[0].keys()) if data else 'No data'}")
except Exception as e:
    print(f"✗ Social Media Content Error: {e}")