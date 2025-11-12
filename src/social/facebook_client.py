import requests
from config import Config
from src.utils.logger import logger, log_activity
from .base import SocialMediaBase

class FacebookClient (SocialMediaBase):
    #Facebook API Client using Graph API

    def __init__(self):
        super().__init__('Facebook')
        self.access_token = Config.META_ACCESS_TOKEN
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.daily_limit = Config.FACEBOOK_DAILY_LIMIT
        self.base_url='https://graph.facebook.com/v18.0'

        if self.access_token and self.page_id:
            logger.info("Facebook Client Initialized")
        else:
            logger.warning("Facebook credentials not configured")

    def post(self, text, media_path=None):
        #Post to Facebook Page
        if not self.access_token or not self.page_id:
            logger.error("Facebook not configured")
            return None
        if not self.check_limit():
            return None
        

        try:
            url = f"{self.base_url}/{self.page_id}/feed"

            #post with or without media

            if media_path:
                #upload photo with caption
                url = f"{self.base_url}/{self.page_id}/photos"