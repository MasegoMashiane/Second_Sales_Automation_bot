import pytest
import responses
from unittest.mock import Mock, patch, MagicMock
from src.social.facebook_client import FacebookClient
from src.social.instagram_client import InstagramClient
from src.social.base import SocialMediaBase

class TestSocialMediaBase:
    def test_check_limit_under(self):
        class TestClient(SocialMediaBase):
            def post(self, text, media_path=None):
                pass
            def get_metrics(self, post_id):
                pass
        client = TestClient('Test')
        client.daily_limit=100
        client.daily_count=50

        assert client.check_limit() is True

    def test_check_limit_reached(self):
        class TestClient(SocialMediaBase):
            def post(self, text, media_path=None):
                pass
            def get_metrics(self, post_id):
                pass
        client = TestClient('Test')
        client.daily_count = 100
        client.daily_limit = 100

        assert client.check_limit() is False

    def test_reset_daily_count(self):
        class TestClient(SocialMediaBase):
            def post(self, text, media_path=None):
                pass
            def get_metrics(self, post_id):
                pass

        client = TestClient('Test')
        client.daily_count = 50
        client.reset_daily_count()

        assert client.daily_count == 0 

class TestFacebookClient:
    def test_init(self, mock_config):
        client = FacebookClient()
        assert client.platform_name == 'Facebook'
        assert client.access_token == mock_config.META_ACCESS_TOKEN
        assert client.page_id == mock_config.FACEBOOK_PAGE_ID

    @responses.activate
    def test_post_text_only(self, mock_config):
        responses.add(
            responses.POST,
            f"https://graph.facebook.com/v18.0/{mock_config.FACEBOOK_PAGE_ID}/feed",
            json={'id':'test_post_123'},
            status=200
        )

        client = FacebookClient()
        post_id = client.post('Test post')

        assert post_id == 'test_post_123'
        assert client.daily_count == 1
    
    @responses.activate
    def test_post_failure(self, mock_config):
        responses.add(
            responses.POST,
            f"https://graph.facebook.com/v18.0/{mock_config.FACEBOOK_PAGE_ID}/feed",
            json={'error': 'Invalid token'},
            status=400
        )

        client = FacebookClient()
        post_id = client.post('Test post')

        assert post_id is None
        assert client.daily_count == 0
        
    @responses.activate
    def test_get_metrics(self, mock_config):
        responses.add(
            responses.GET,
            'https://graph.facebook.com/v18.0/test_post_123',
            json={
                'likes':{'summary':{'total_count':10}},
                'comments': {'summary': {'total_count': 5}},
                'shares': {'count':2}
            },
            status=200
        )

        client = FacebookClient()
        metrics = client.get_metrics('test_post_123')

        assert metrics['likes'] == 10
        assert metrics['comments'] == 5
        assert metrics['shares'] == 2

class TestInstagramClient:
    def Test_init(self, mock_config):
        client = InstagramClient()
        assert client.platform_name == 'Instagram'
        assert client.account_id == mock_config.INSTAGRAM_ACCOUNT_ID


    def test_post_without_media(self, mock_config):
        client = InstagramClient()
        post_id = client.post('Test post')

        assert post_id is None

        