import pytest
from unittest.mock import Mock, patch
from datetime import datetime

class TestEndToEndSalesCampaign: 
    @patch ('src.campaigns.sales_campaign.SheetsManager')
    @patch ('src.campaigns.sales_campaign.EmailClient')
    @patch ('src.campaigns.sales_campaign.time.sleep')
    def test_full_sales_workflow(self, mock_sleep, mock_email, mock_sheets):
        from src.campaigns.sales_campaign import SalesCampaign        

        #Mock data
        leads = [
            {
            'Name': 'Test User',
            'Email': 'test@example.com',
            'Company': 'TestCo',
            'Industry': 'Tech',
            'Status': 'Pending',
            'Last Contact': '',
            'Stage': 0
            }
        ]

        #Setup Mocks
        mock_sheets_instance = mock_sheets.return_value
        mock_sheets_instance.get_sales_leads.return_value = leads
        mock_sheets_instance.update_lead_status.return_value = True

        mock_email_instance = mock_email.return_value
        mock_email_instance.send.return_value = True

        #Run Campaign
        campaign = SalesCampaign()
        campaign.run()

        #Verify workflow
        assert mock_sheets_instance.get_sales_leads.called
        assert mock_email_instance.send.called
        assert mock_sheets_instance.update_lead_status.called

class TestEndToEndSocialCampaign:
    
    @patch('src.campaigns.social_campaign.SheetsManager')
    @patch('src.campaigns.social_campaign.FacebookClient')
    @patch('src.campaigns.social_campaign.InstagramClient')
    @patch('src.campaigns.social_campaign.time.sleep')
    def test_full_social_workflow(self, mock_sleep, mock_instagram, mock_facebook, mock_sheets):
        from src.campaigns.social_campaign import SocialCampaign
        now = datetime.now()
        posts = [
            {
                'Date': now.strftime(),
                'Time': now.strftime(),
                'Platform': 'Facebook',
                'Text': 'Test post',
                'Media': '',
                'Hashtags': '#test',
                'Status': 'Pending',
                'Posted Time': '',
                'Post ID': ''
                }
            ]
        
        # Setup Mocks
        mock_sheets_instance = mock_sheets.return_value
        mock_sheets_instance.get_social_posts.return_value = posts
        mock_sheets_instance.mark_post_as_sent.return_value = True

        mock_facebook_instance = mock_facebook.return_value
        mock_facebook_instance.post.return_value = 'test_post_123'

        #run campaign
        campaign = SocialCampaign()
        campaign.run()

        #verify
        assert mock_sheets_instance.get_social_posts.called
        assert mock_facebook_instance.post.called
        assert mock_sheets_instance.mark_post_as_sent.called