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

Project Folder Structure


sales-automation/
config/              Configuration and credentials
    __init__.py
    credentials.json
    settings.py
src/                 Source code
   database/        Google Sheets integration
   email/           Email client and templates
   social/          Social media clients
   campaigns/       Campaign logic
   utils/           Utilities (logging, scheduling)
       __init__.py
       logger.py
       scheduler.py
data/                Logs and data files
    logs/
       activity.csv
       automation.log
    templates/
        sales_leads_template.csv
        social_posts_template.csv
tests/               Unit tests
    __inti__.py
    conftest.py       testing configurations and credentials
    test_campaigns.py    
    test_email.py
    test_social.py
scripts/
    generate_example_data.py        Mock Data for testing
    setup.py
    test_connections.py
main.py              Main entry point
run_scheduler.py     Scheduled automation
requirements.txt



Setup Instructions

1. Install Dependencies
pip install -r requirements.txt
still working on this

2. Configure Environment
cp .env.example .env
Edit .env with your credentials


3. Setup Google Sheets API
    3.1. Go to [Google Cloud Console](https://console.cloud.google.com)
    3.2. Create project → Enable Google Sheets API
    3.3. Create Service Account → Download JSON
    3.4. Save as `config/credentials.json`
    3.5. Share your sheets with service account email

5. Create Google Sheets

Sales Leads Sheet:
| Name | Email | Company | Industry | Status | Last Contact | Stage |

Media Content Sheet:
| Date | Time | Platform | Text | Media | Hashtags | Status | Posted Time | Post ID |



Usage:
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
... can be changed to whatever time of your choice based on analytics
Sales campaigns daily at 9 AM
Social posts every 30 minutes
Metrics collection daily at 6 PM

Testing
python -m pytest tests/

Logs
All activity is logged to:
data/logs/automation.log - Detailed logs
data/logs/activity.csv - Activity summary

Free Tier Limits
- Gmail: 500 emails/day
