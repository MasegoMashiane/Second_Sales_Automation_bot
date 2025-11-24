import pytest
from unittest.mock import Mock, patch, MagicMock
from src.database.sheets_manager import SheetsManager

class TestSheetsManager:
    @patch('src.database.sheets_manager.gspread')
    @patch('src.database.sheets_manager.ServiceAccountCredentials')
    def test_int(self, mock_creds, mock_gspread, mock_config):
        mock_client= MagicMock()
        mock_gspread.authorize.return_value = mock_client

        manager = SheetsManager()
        assert manager.client == mock_client
    
    @patch('src.database.sheets_manager.gspread')
    @patch('src.database.sheets_manager.ServiceAccountCredentials')
    def test_get_sales_leads(self, mock_config, mock_gspread, mock_creds, sample_leads):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = sample_leads

        mock_client = MagicMock()
        mock_client.open.return_value.sheet1 = mock_sheet
        mock_gspread.authorize.return_value = mock_client

        manager = SheetsManager()
        leads = manager.get_sales_leads()

        assert len(leads) == 2
        assert leads[0]['Name'] == 'Alice'
        
    @patch('src.database.sheets_manager.gspread')
    @patch('src.database.sheets_manager.ServiceAccountCredentials')
    def test_update_lead_status(self, mock_config, mock_gspread, mock_creds, sample_posts):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = sample_posts

        mock_client = MagicMock()
        mock_client.open.return_value.sheet1 = mock_sheet
        mock_gspread.authorize.return_value = mock_client

        manager = SheetsManager()
        result = manager.update_lead_status(2, 'Contacted', 1)

        assert result is True
        assert mock_sheet.update_cell.call_count == 3

    @patch('src.database.sheets_manager.gspread') 
    @patch('src.database.sheets_manager.ServiceAccountCredentials')
    def test_get_social_posts(self, mock_creds, mock_gspread, mock_config, sample_posts):
        mock_sheet = MagicMock()
        mock_sheet.get_all_records.return_value = sample_posts

        mock_client = MagicMock()
        
        mock_client.open.return_value.sheet1 = mock_sheet
        mock_gspread.authorize.return_value = mock_client

        manager = SheetsManager()
        posts = manager.get_social_post()

        assert len(posts) == 3
        assert posts[0]['Platform'] == 'Facebook'