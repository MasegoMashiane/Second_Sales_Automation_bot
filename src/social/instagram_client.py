import requests
import time
from config import Config
from src.utils.logger import logger, log_activity
from .base import SocialMediaBase

class InstagramClient(SocialMediaBase):
    #Instagram API using Graph API(Business account)

    def __init__(self):
        super().__init__('Instagram')
        self.access_token = Config.META_ACCESS_TOKEN
        self.account_id = Config.INSTAGRAM_ACCOUNT_ID
        self.daily_limit = Config.INSTAGRAM_DAILY_LIMIT
        self.base_url = 'https://graph.facebook.com/v18.0'

        if self.access_token and self.account_id:
            logger.info("Instagram client initialized")
        else:
            logger.warning(f"Instagram credentials not configured")
    
    def post(self, text, media_path=None):
        #Post to Insta require media, it doesn't support text only posts
        if not self.access_token or not self.account_id:
            logger.error("Instagram not configured")
            return None
        
        if not self.check_limit():
            return None
        
        if not media_path:
            logger.error("Instagram requires media(image or video)")
            return None
        
        try:
            #create media container
            container_id=self._create_media_container(text, media_path)
            if not container_id:
                return None
            
            #Wait for media to process
            time.sleep(5)

            #Publish the container
            post_id = self._publish_container(container_id)

            if post_id:
                self.daily_count+=1
                logger.info(f"Instagram post published: {post_id}({self.daily_count}/{self.daily_limit})")
                log_activity('Instagram', 'Success', f'Post ID:{post_id}')

                return post_id
        except Exception as e:
            logger.error(f"Instagram post failed: {e}")
            log_activity('Instagram', 'Failed', str(e))
            return None
        
    def _create_media_container(self, caption, media_path):
        url=f"{self.base_url}/{self.account_id}/media"

        #Image. Video requires different params
        data={
            'image_url': media_path, #Must be publicly accessible url
            'caption': caption,
            'access_token': self.access_token
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        result= response.json
        
        return result.get('id')
    
    def get_metrics(self, post_id):
        
        try:
            url=f"{self.base_url}/{post_id}/insights"
            params={
                'metric': "engagement,impressions,reach,saved",
                'access_token':self.access_token
            }

            response=requests.get(url, params=params)
            response.raise_for_status()
            data=response.json()

            metrics={}
            for item in data.get('data',[]):
                metrics[item['name']]=item['values'][0]['value']

            logger.info(f"Instagram post {post_id} metrics: {metrics}")
            return metrics
        
        except Exception as e:
            logger.error(f"Failed to get Instagram metrics for {post_id}: {e}")
            return None
            

        