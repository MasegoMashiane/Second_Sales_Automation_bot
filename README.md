Sales Automation
- Multi-stage email campaigns (initial + 2 follow-ups)
- Personalized email templates
- Gmail integration (500 emails/day)
- Google Sheets CRM integration
- Automated follow-up scheduling

Social Media Automation
- Twitter/X posting with media
- Schedule posts from Google Sheets
- Engagement metrics tracking
- Multi-platform ready (Instagram, LinkedIn)

System Features
- Comprehensive logging (file + CSV)
- Error handling & notifications
- Rate limiting & daily quotas
- Scheduled task execution

Project Structure


sales-automation/
├── config/              # Configuration and credentials
├── src/                 # Source code
│   ├── database/        # Google Sheets integration
│   ├── email/           # Email client and templates
│   ├── social/          # Social media clients
│   ├── campaigns/       # Campaign logic
│   └── utils/           # Utilities (logging, scheduling)
├── data/                # Logs and data files
├── tests/               # Unit tests
├── scripts/             # Setup and utility scripts
├── main.py              # Main entry point
└── run_scheduler.py     # Scheduled automation


Setup Instructions

1. Install Dependencies
pip install -r requirements.txt


2. Configure Environment
cp .env.example .env
Edit .env with your credentials


3. Setup Google Sheets API
    1. Go to [Google Cloud Console](https://console.cloud.google.com)
    2. Create project → Enable Google Sheets API
    3. Create Service Account → Download JSON
    4. Save as `config/credentials.json`
    5. Share your sheets with service account email

4. Setup Twitter API

    1. Go to [developer.twitter.com](https://developer.twitter.com)
    2. Create app (Free tier)
    3. Get API keys and add to `.env`

5. Create Google Sheets

Sales Leads Sheet:
| Name | Email | Company | Industry | Status | Last Contact | Stage |
|------|-------|---------|----------|--------|--------------|-------|

Social Media Content Sheet:
| Date | Time | Platform | Text | Media | Hashtags | Status | Posted Time | Post ID |
|------|------|----------|------|-------|----------|--------|-------------|---------|

Usage

To run Individual Campaigns
Run sales campaign
python main.py sales

Run social media campaign
python main.py social

Collect metrics
python main.py metrics



To run all campaigns once
python main.py


Run Scheduled Automation
python run_scheduler.py


This will run:
- Sales campaigns daily at 9 AM
- Social posts every 30 minutes
- Metrics collection daily at 6 PM

Testing
python -m pytest tests/


Logs

All activity is logged to:
- data/logs/automation.log - Detailed logs
- data/logs/activity.csv - Activity summary

Free Tier Limits

- Gmail: 500 emails/day
- Twitter: 50 tweets/day