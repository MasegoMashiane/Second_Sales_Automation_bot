import pytest
from unittest.mock import Mock, patch, MagicMock
from src.email.email_client import EmailClient
from src.email.templates import EmailTemplates

#testing email functionality

class TestEmailClient:
    def test_init(self, mock_config):
        #Test EmailClient initialization
        client = EmailClient()
        assert client.sender == mock_config.EMAIL_ADDRESS
        assert client.password == mock_config.EMAIL_PASSWORD
        assert client.daily_count == 0
        assert client.daily_limit == mock_config.EMAIL_DAILY_LIMIT

    @patch('smtplib.SMTP_SSL')
    def test_send_email_success(self, mock_smtp, mock_config):
        #setup
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        #Send Email
        client = EmailClient()
        result = client.send(
            'test@example',
            'Test Subject', 
            '<p> Test Body</p>',
        )

        #Assertions
        assert result is True
        assert client.daily_count == 1
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @patch('smtplib.SMTP_SSL')
    def test_send_email_failure(self, mock_smtp, mock_config):
        mock_server = MagicMock()
        mock_server.send_message.side_effect = Exception('SMTP error')
        mock_smtp.return_value.__enter__.return_value = mock_server

        #send Email
        client = EmailClient()
        result = client.send(
            'test@example',
            'Test Subject', 
            '<p> Test Body</p>',
        )

        #Assertions
        assert result is False
        assert client.daily_count == 0

    def test_daily_limit(self, mock_config):
        client = EmailClient()
        client.daily_count = client.daily_limit

        result = client.send(
            'test@example.com',
            'Test Subject',
            '<p>Test body</p>'      
        )

        assert result is False

    def test_reset_daily_count(self, mock_config):
        client = EmailClient()
        client.daily_count = 100
        client.reset_daily_count()

        assert client.daily_count == 0 

class  TestEmailTemplates:
    def test_get_initial_template(self):
        template = EmailTemplates.get(
            'initial',
            name='John',
            company='TestCorp',
            industry='SaaS',
            value_prop='increase revenue',
            sender_name='Bob'
        )

        assert 'john' in template
        assert 'TestCorp' in template
        assert 'SaaS' in template
        assert 'increase revenue' in template
        assert 'Bob' in template

    def test_get_followup_1_template(self):
        template = EmailTemplates.get(
        'followup_1',
        name='Jane',
        similar_company='CompanyX',
        result='40% growth',
        sender_name='Bob'
        )

        assert 'Jane' in template
        assert 'CompanyX' in template
        assert '40% growth'
        assert 'Bob' in template

    def test_get_followup_2_template(self):
        template = EmailTemplates.get(
            'followup_2',
            name='Alice',
            resource_link='https://example.com',
            sender_name='Bob'
        )

        assert 'Alice' in template
        assert 'https://example.com' in template
        assert 'Bob' in template