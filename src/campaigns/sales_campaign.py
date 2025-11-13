import time
from datetime import datetime
from src.database.sheets_manager import SheetsManager
from src.email.email_client import EmailClient
from src.email.templates import EmailTemplates
from src.utils.logger import logger

class SalesCampaign:
    #Manageing sales campaign

    def __init__(self):
        self.sheets=SheetsManager()
        self.email=EmailClient()

    def run(self):
        #Execution of sales campaigns
        logger.info("=== Starting Sales Campaign ===")
        leads = self.sheets.get_sales_leads()

        for i, lead in enumerate(leads):
            #Skip if contacted today
            if self._contacted_today(lead):
                continue

            stage = int(lead.get('stage', 0))

            #Determine emain type
            if stage == 0:
                email_data = self._prepare_intitial_email(lead)
            elif stage == 1:
                email_data = self._prepare_followup_1(lead)
            elif stage == 2:
                email_data=self._prepare_followup_2(lead)
            else:
                continue #campign complete

            #send email
            success = self.email.send(
                lead['Email'],
                email_data['subject'],
                email_data['body']
            )

            if success:
                self.sheets.update_lead_status(i+2, 'contacted', i+1)
                logger.info(f"Sent stage {stage} email to {lead['Name']}")

            time.sleep(10)

        logger.info("=== Sales Campaign Complete ===")

    def _Contacted_today(self, lead):
        #Check if lead was contacted today
        if lead.get('Status') != 'Contacted':
            return False
        
        last_contact = lead.get('last Contact', '')
        if not last_contact:
            return False
        
        try:
            contact_date = datetime.fromisoformat(last_contact).date()
            return contact_date == datetime.now().date()
        except:
            return False
        
    def _prepare_intitial_email(self, lead):
        return {
            'subject': f"Quick Question about {lead['Company']}",
            'body':EmailTemplates.get(
                'initial', 
                name=lead['Name'],
                company=lead['Company'],
                industry=lead.get('industry', 'our industry'),
                value_prop="Increase revenue by 30%",
                sender_name="Name"
            )
        }

    def _prepare_followup_1(self, lead):
        return{
            'subject': f"Quick Question about {lead['Company']}",
            'body':EmailTemplates.get(
                'followup_1', 
                name=lead['Name'],
                similar_Company="CompanyX",
                result="40% growth",
                sender_name="Name"
            )
        }
    
    def _prepare_followup_2(self, lead):
        return{
            'subject': f"Quick Question about {lead['Company']}",
            'body':EmailTemplates.get(
                'followup_2', 
                name=lead['Name'],
                industry=lead.get('industry', 'our industry'),
                resource_link="https://motherhoodafrica.org",
                sender_name="Name"
            )
        }




    