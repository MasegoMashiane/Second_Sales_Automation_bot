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
        posts = self.sheets.get_social_posts()
        current_time = datetime.now()

        for i, post in enumerate(posts):
            if posts.get('Status') == 'Posted':
                continue

            if self._is_time_to_post(post, current_time):
                self._post_content(post, i + 2)
                time.sleep(2)

            logger.info("=== Social Media Campaign Complete ===")

    def _is_time_to_post(self, post, currnt_time):
        #Check if it is time to post

        try:
            scheduled_time = datetime.strptime(
                f"{post['Date']} {post['Time']}","%Y-%m-%d %H:%M" 
            )