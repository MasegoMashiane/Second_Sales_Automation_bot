import pytest
from unittest.mock import Mock, patch, MagicMock
from src.email.email_client import EmailClient
from src.email.templates import EmailTemplates

class TestEmailClient:
    def test_init(self, mock_config):
        #Test EmailClient initialization
        client = EmailClient()
        assert client.sender == mock_config.EMAIL_ADDRESS
        assert client.password == mock_config.EMAIL_PASSWORD
        assert client.daily_count == 0
        assert client.daily_limit == mock_config.EMAIL_DAILY_LIMIT

    @patch('smtplib.SMTP_SSL')
    def test_send_email_success(self, moock_smtp, mock_config):
        mock_server = MagicMock()

        mock_c