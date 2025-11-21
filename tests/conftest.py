import pytest
import os 
from pathlib import Path
from unittest.mock import Mock, MagicMock

#Test Env
 
os.environ['EMAIL_ADDRESS'] = 'test@example.com'
os.environ['EMAIL_PASSWORD'] = 'test_password'
os.environ['GOOGLE_SHEETS_CREDENTIALS'] = 'test_credentials.json'
os.environ['META_ACCESS_TOKEN'] = 'test_meta_token'
os.environ['FACEBOOK_PAGE_ID'] = 'test_page_id'
os.environ['INSTAGRAM_ACCOUNT_ID'] = 'test_instagram_id'
os.environ['LINKEDIN_ACCESS_TOKEN'] = 'test_linkedin_token'
os.environ['LINKEDIN_PERSON_URN'] = 'test_person_urn'

@pytest.fixture
def mock_config():
    from config import Config
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return Config

@pytest.fixture
def sample_lead():
    return{
        'Name': 'John Doe',
        'Email': 'john@example.com',
        'Company': 'TestCorp',
        'Industry': 'Saas',
        'Status': 'Pending',
        'Last Contact': '',
        'Stage': 0
    }

@pytest.fixture
def sample_leads():
    return[{
        'Name': 'John Doe',
        'Email': 'john@example.com',
        'Company': 'TestCorp',
        'Industry': 'Saas',
        'Status': 'Pending',
        'Last Contact': '',
        'Stage': 0
    },
    {
        'Name': 'Jane Smith',
        'Email': 'jane@example.com',
        'Company': 'StartupX',
        'Industry': 'E-commerce',
        'Status': 'Contacted',
        'Last Contact': '2025-11-13',
        'Stage': 1
    }]

@pytest.fixture
def sample_post():
    return {
        'Date': '2025-11-14',
        'Time': '09:00',
        'Platform': 'Facebook',
        'Text': 'Test post',
        'Media': '',
        'Hashtags': '#test',
        'Status': 'Pending',
        'Posted Time': '',
        'Post ID': '',
    }

@pytest.fixture
def sample_posts():
    return[
    {
        'Date': '2025-11-14',
        'Time': '09:00',
        'Platform': 'Facebook',
        'Text': 'Test Facebook post',
        'Media': '',
        'Hashtags': '#test',
        'Status': 'Pending',
        'Posted Time': '',
        'Post ID': '',
    },
    {
        'Date': '2025-11-14',
        'Time': '10:00',
        'Platform': 'Instagram',
        'Text': 'Test Instagram post',
        'Media': 'https://example.com/image.jpg',
        'Hashtags': '#test',
        'Status': 'Pending',
        'Posted Time': '',
        'Post ID': '',
    },
]

@pytest.fixture
def mock_sheets_manager(mocker, sample_leads, sample_posts):
    mock = mocker.Mock()
    mock.get_sales_leads.return_value = sample_leads
    mock.get_social_posts.return_value = sample_posts
    mock.update_lead_status.return_value = True
    mock.mark_post_as_sent.return_value = True
    return mock

@pytest.fixture
def mock_email_client(mocker):
    mock = mocker.Mock()
    mock.send.return_value = True
    mock.daily_count = 0
    mock.daily_limit = 450
    return mock

@pytest.fixture
def mock_instagram_client(mocker):
    mock = mocker.Mock()
    mock.post.return_value = 'test_ig_post_456'
    mock.get_metrics.return_value = {'likes':10, 'comments':5, 'shares':2}
    mock.check_limit.return_value = True
    return mock

@pytest.fixture
def mock_instagram_client_analytics(mocker):
    mock = mocker.Mock()
    mock.post.return_value = 'test_ig_post_456'
    mock.get_metrics.return_value = {'engagement':100, 'impressions':500}
    mock.check_limit.return_value = True
    return mock