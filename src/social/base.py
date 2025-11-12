from abc import ABC, abstractmethod
from src.utils.logger import logger

class SocialMediaBase(ABC):
    #base class for social media clients
    def __init__(self, platform_name):
        self.platform_name= platform_name
        self.daily_count = 0
        self.daily_limit = 0

        @abstractmethod
        def post(self, text, media_path=None):
            pass

        def check_limit(self):
            if self.daily_count>=self.daily_limit:
                logger.warning(f"{self.platform_name} daily limit reached ({self.daily_limit})")
                return False
            return True
        
        def reset_daily_count(self):
            self.daily_count = 0
            logger.info(f"{self.platform_name} counter reset")

            #ENFORCING POLYMORPHISM FOR THE DIFFERENT PLATFORMS BEING INTERACTED WITH

            