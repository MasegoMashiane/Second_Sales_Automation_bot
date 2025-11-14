#Main entry point

from config import Config
from src.campaigns.sales_campaign import SalesCampaign
from src.campaigns.social_campaign import SocialCampaign
from src.utils.logger import logger

def run_sales():
    #run sales campaign
    try:
        campaign = SalesCampaign()
        campaign.run()
    except Exception as e:
        logger.error(f"Sales campaign error: {e}")

def run_social():
    #run social media campaign
    try:
        campaign = SocialCampaign()
        campaign.run()
    except Exception as e:
        logger.error(f"Social campaign error: {e}")

def collect_metrics():
    #Collecting social media metrics
    try:
        campaign = SalesCampaign()
        campaign.collect_metrics()
    except Exception as e:
        logger.error(f"Metrics collection error: {e}")

if __name__ == "__main__":
    import sys

    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv)>1:
        command = sys.argv[1]
        if command == "sales":
            run_sales()
        elif command == "social":
            run_social()
        elif command == "merics":
            collect_metrics()
        else:
            print("Usage: python main.py [sales| social| metrics]")

    else:
        print("Running all campaigns...")
        run_sales()
        run_social()