import pytest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime
from src.campaigns.sales_campaign import SalesCampaign
from src.campaigns.social_campaign import SocialCampaign

class TestSalesCampaign:

    @patch('src.campaigns.sales_campaign.SheetsManager')
    @patch('src.campaigns.sales_campaign.EmailClient')
    def test_init(self, mock_email, mock_sheets, sample_lead):
        campaign = SalesCampaign()

        assert campaign.sheets is not None
        assert campaign.email is not None

  
    @patch('src.campaigns.sales_campaign.SheetsManager')
    @patch('src.campaigns.sales_campaign.EmailClient')
    def test_contacted_today(self, moock_email, mock_sheets, sample_lead):
        campaign = SalesCampaign()

        assert campaign._Contacted_today(sample_lead) is False

        sample_lead['Status'] = 'Contacted'
        sample_lead['Last Contact'] = datetime.now().isoformat()
        assert campaign._Contacted_today(sample_lead) is True


    @patch('src.campaigns.sales_campaign.SheetsManager')
    @patch('src.campaigns.sales_campaign.EmailClient')
    @patch('src.campaigns.sales_campaign.time.sleep')
    def test_run_campaign(self, mock_sleep, mock_email, mock_sheets,sample_leads):
        #setup 
        mock_sheets_instance = mock_sheets.return_value
        mock_sheets_instance.get_sales_leads.return_value = sample_leads
        mock_sheets_instance.update_lead_status.return_value = True
        
        mock_email_instance = mock_email.return_value
        mock_email_instance.send.return_value = True

        #run campaign
        campaign = SalesCampaign()
        campaign.run()

        #verify emails were sent
        assert mock_email_instance.send.called

class TestSocialCampaign:



    @patch('src.campaigns.social_campaign.SheetsManager')
    @patch('src.campaigns.social_campaign.FacebookClient')
    @patch('src.campaigns.social_campaign.InstagramClient')
    def test_init(self, mock_ig, mock_fb, mock_sheets):
        campaign = SocialCampaign()

        assert campaign.sheets is not None
        assert campaign.facebook is not None
        assert campaign.instagram is not None

    @patch('src.campaigns.social_campaign.SheetsManager')
    @patch('src.campaigns.social_campaign.FacebookClient')
    @patch('src.campaigns.social_campaign.InstagramClient')
    def test_is_time_to_post(self, mock_ig, mock_fb, mock_sheets):
        campaign = SocialCampaign()
        #current time post
        now = datetime.now()
        post = {
            'Date': now.strftime('%Y-%m-%d'),
            'Time': now.strftime('%H:%M')
        }
        assert campaign._is_time_to_post(post, now) is True

        #Future time post
        future_post = {
            'Date': '2025-12-31',
            'Time': '23:59'
        }
        assert campaign._is_time_to_post(future_post, now) is False

    @patch('src.campaigns.social_campaign.SheetsManager')
    @patch('src.campaigns.social_campaign.FacebookClient')
    @patch('src.campaigns.social_campaign.InstagramClient')
    @patch('src.campaigns.social_campaign.time.sleep')
    def test_post_to_facebook(self, mock_sleep, mock_ig, mock_fb, mock_sheets, sample_post):
        
        #Setup
        mock_facebook_instance = mock_fb.return_value
        mock_facebook_instance.post.return_value = 'test_fb_post_123'

        mock_sheets_instance = mock_sheets.return_value
        mock_sheets_instance.mark_post_as_sent.return_value = True

        #Post Content
        campaign = SocialCampaign()
        campaign._post_content(sample_post, 2)

        #Verify
        mock_facebook_instance.post.assert_called_once()
        mock_sheets_instance.mark_post_as_sent.assert_called_once()
    
    @patch('src.campaigns.social_campaign.SheetsManager')
    @patch('src.campaigns.social_campaign.FacebookClient')
    @patch('src.campaigns.social_campaign.InstagramClient')
    def test_collect_metrics(self, mock_ig, mock_fb, mock_sheets, sample_posts):
        
        #Setup
        mock_sheets_instance = mock_sheets.return_value
        mock_sheets_instance.get_metrics.return_value = {'likes': 10}

        #Collect Metrics
        campaign = SocialCampaign()
        metrics = campaign.collect_metrics()

        #Verify
        assert mock_sheets_instance.get_social_posts.called