import time
from datetime import datetime
from src.database.sheets_manager import SheetsManager
from src.social.facebook_client import FacebookClient
from src.social.instagram_client import InstagramClient
from src.utils.logger import logger


class SocialCampaign:
    def __init__(self):
        self.sheets = SheetsManager()
        self.facebook = FacebookClient()
        self.instagram = InstagramClient()

    def run(self):
        #Executing social media campaign
        logger.info("=== Starting Social Media Campaign === ")
        posts = self.sheets.get_social_post()
        current_time = datetime.now()

        for i, post in enumerate(posts):
            if post.get('Status') == 'Posted':
                continue

            if self._is_time_to_post(post, current_time):
                self._post_content(post, i + 2)
                time.sleep(2)

            logger.info("=== Social Media Campaign Complete ===")

    def _is_time_to_post(self, post, current_time):
        #Check if it is time to post

        try:
            scheduled_time = datetime.strptime(
                f"{post['Date']} {post['Time']}","%Y-%m-%d %H:%M" 
            )
            time_diff = (current_time - scheduled_time).total_seconds()/60
            return -5 <= time_diff <= 5
        except:
            return False
        
    def _post_content(self, post, row_num):
        platform = post['Platform'].lower()
        text = post['Text']
        hashtags = post.get('Hashtags', '')
        media = post.get('Media', '')
        full_text = f"{text}\n\n{hashtags}".strip()

        post_id = None

        if platform == 'facebook':
            post_id = self.facebook.post(full_text, media if media else None)
            platform_name ='Facebook'

        elif platform == 'instagram':
            if not media:
                logger.error(f"Row {row_num}: Instagram requires media")
                return
            post_id = self.instagram.post(full_text, media)
            platform_name = 'Instagram'

        #elif platform =='linkedin':
        else:
            logger.error(f"Unknown platform: {platform}")
            return
        
        if post_id:
            self.sheets.mark_post_as_sent(row_num, platform_name, post_id)
            logger.info(f"Posted to{platform_name}: {text[:50]}...")


    def collect_metrics(self):
        logger.info("=== Collecting Social Metrics ===")
        posts = self.sheets.get_social_post()

        for post in posts:
            if post.get('Status') == 'Posted' and post.get('Post ID'):
                platform = post['Platform'].lower()
                post_id = post['Post ID']

                metrics = None

                if platform == 'facebook':
                    metrics = self.facebook.get_metrics(post_id)
                elif platform == 'instagram':
                    metrics = self.instagram.get_metrics(post_id)
                #LinkedIn

                if metrics:
                    logger.info(f"{platform.title()} post{post_id}:{metrics}")

                time.sleep(1)

                
        