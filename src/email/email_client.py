import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Config import Config
from src.utils.logger import logger, log_activity
from .templates import EmailTemplates

class EmailClient:
    #Handle email sending operations

    def __init__(self):
        self.sender = Config.EMAIL_ADDRESS
        self.password = Config.EMAIL_PASSWORD
        self.daily_count = 0
        self.daily_limit = Config.EMAIL_DAILY_LIMIT

    def send(self, to_email, subject, body_html):
        if self.daily_count>=self.daily_limit:
            logging.warning(f"Daily limit reached ({self.daily_limit})")
            return False
            
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To'] = to_email
        msg['subject'] = subject
        msg.attach(MIMEText(body_html, 'html'))

        try: 
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)

                self.daily_count += 1
                logging.info(f"Email sent to {to_email} ({self.daily_count}/{self.daily_limit})")
                log_activity('Email', 'success', f'To: {to_email}, Subject: {subject} ')
                return True
            
        except Exception as e:
            logging.error(f'Email failed to {to_email}: {e}')
            log_activity('Email', 'failed', f'{to_email} - {str(e)}')
            return False
        
    def reset_daily_count(self):
        self.daily_count = 0
        logging.info("Email counter reset")
