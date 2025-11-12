import os
from pathlib import Path
from dotenv import load_dotenv

#Load env variables

load_dotenv()

class Config:
    #PATHS
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    LOGS_DIR = DATA_DIR / 'logs'


    #Configurations for Emails
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_DAILY_LIMIT = int(os.getenv('EMAIL_DAILY_LIMIT'))

    #CONFIGURATIONS FOR GOOGLE SHEETS
    GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    SALES_SHEET_NAME = os.getenv('SALES_SHEET_NAME')
    SOCIAL_SHEET_NAME = os.getenv('SOCIAL_SHEET_NAME')

    #CONFIGURATIONS FOR FACEBOOK/INSTAGRAM (META) API
    META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
    
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    FACEBOOK_DAILY_LIMIT = int(os.getenv('FACEBOOK_DAILY_LIMIT'))
    
    INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')
    INSTAGRAM_DAILY_LIMIT = int(os.getenv('INSTAGRAM_DAILY_LIMIT'))

    #Configurations for LinkedIn API
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
    LINKEDIN_PERSON_URN = os.getenv('LINKEDIN_PERSON_URN')
    LINKEDIN_ORGANIZATION_URN = os.getenv('LINKEDIN_ORGANIZATION_URN')
    LINKEDIN_DAILY_LIMIT =int(os.getenv('LINKEDIN_DAILY_LIMIT'))

    #LOGGING CONFIGURATIONS
    LOG_FILE = LOGS_DIR / 'automation.log'
    ACTIVITY_LOG = LOGS_DIR / 'activity.csv'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        #validating required configuration
        required = [
            'Email_ADDRESS',
            'EMAIL_PASSWORD',
            'GOOGLE_SHEETS_CREDENTIALS'
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required config: {','.join(missing)}")