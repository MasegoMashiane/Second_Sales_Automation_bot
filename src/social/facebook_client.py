import requests
import logging
from Config import Config
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
            logging.info("Facebook Client Initialized")
        else:
            logging.warning("Facebook credentials not configured")

    def post(self, text, media_path=None):
        #Post to Facebook Page
        response = None
        if not self.access_token or not self.page_id:
            logging.error("Facebook not configured")
            return None
        if not self.check_limit():
            return None
        

        try:
            url = f"{self.base_url}/{self.page_id}/feed"

            #post with or without media

            if media_path:
                #upload photo with caption
                url = f"{self.base_url}/{self.page_id}/photos"

                with open(media_path, 'rb') as image_file:
                    files = {'source': image_file}
                    data = {
                        'message': text,
                        'access_token': self.access_token
                    }
                response = requests.post(url, data=data, files=files)
            else:
            # Normal text post
                data = {
                    "message": text,
                    "access_token": self.access_token,
                }
                response = requests.post(url, data=data)
                
            response.raise_for_status()
            result = response.json()
            post_id = result.get('id') or result.get('post_id')

            self.daily_count+= 1
            logging.info(f"Facebook post published: {post_id} ({self.daily_count}/{self.daily_limit})")
            log_activity('facebook', 'success', f'Post ID: {post_id}')
            return post_id
        except Exception as e:
            logging.error(f"Facebook post failed:{e}")
            log_activity('facebook', 'Failed', str(e))
            return None
        
    def get_metrics(self, post_id):
        #Post metrics
        try:
            url = f"{self.base_url}/{post_id}"
            params = {
                'fields': 'likes.summary(true), comments.summary(true), shares',
                'access_token': self.access_token
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            metrics = {
                'likes': data.get('likes', {}).get('summary', {}).get('total_count', 0),
                'comments': data.get('comments', {}).get('summary', {}).get('total_count', 0),
                'shares': data.get('shares', {}).get('count', 0)
            }

            logging.info(f"Facebook post {post_id} metrics: {metrics}")
            return metrics
        
        except Exception as e:
            logging.error(f"Failed to get Facebook metrics for {post_id}: {e}")
            return None