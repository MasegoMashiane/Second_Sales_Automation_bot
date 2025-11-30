import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from Config import Config
from src.utils.logger import logger

class SheetsManager:
    #Managing Google shees opertaions

    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        #Connecting to google sheets API
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                Config.GOOGLE_SHEETS_CREDENTIALS, scope
            )
            self.client = gspread.authorize(creds)
            logger.info("Connected to Google Sheets")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            raise



    def get_sales_leads(self):
        try:
            sheet = self.client.open(Config.SALES_SHEET_NAME).sheet1
            return sheet.get_all_records()
        
        except Exception as e:
            logger.error(f"Error reading sales leads: {e}")
            return []



    def update_lead_status(self, row_num, status, stage=None):
        #Updating lead status
        
        try:
            sheet = self.client.open(Config.SALES_SHEET_NAME).sheet1
            sheet.update_cell(row_num, 5, status)
            sheet.update_cell(row_num, 6, datetime.now().isoformat())
            if stage is not None:
                sheet.update_cell(row_num, 7, stage)
            logger.info(f"Updating lead row {row_num} was succesful")
            return True
        
        except Exception as e:
            logger.error(f"Error Updating lead: {e}")
            return False
        

    def get_social_post(self):
        #Get scheduled social media posts
        
        try:
            sheet = self.client.open(Config.SOCIAL_SHEET_NAME).sheet1
            return sheet.get_all_records()
        
        except Exception as e:
            logger.error(f"Error reading social posts: {e}")
            return []
        
    def mark_post_as_sent(self, row_num, platform, post_id=None):
        
        try: 
            sheet = self.client.open(Config.SOCIAL_SHEET_NAME).sheet1
            sheet.update_cell(row_num, 7, 'Posted')
            sheet.update_cell(row_num, datetime.now().isoformat)
            if post_id:
                sheet.update_cell(row_num, 9, post_id)
            logger.info(f"Marked post row {row_num} as sent on {platform}")
            return True
        
        except Exception as e:
            logger.error(f"Error marking post as sent: {e}")
            return False