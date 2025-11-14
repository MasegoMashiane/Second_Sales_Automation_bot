import schedule
import time
from main import run_social, run_sales, collect_metrics
from src.utils.logger import logger

def main():
    #setup and run scheduler

    #schedule tasks
    schedule.every().day.at("09:00").do(run_sales)
    schedule.every(30).minutes.do(run_social)
    schedule.every().day.at("18:00").do(collect_metrics)

    logger.info("Automation Scheduler Started")
    logger.info("="*50)
    logger.info("Sales campaigns: Daily at 09:00")
    logger.info("Social posts: Every 30 minutes")
    logger.info("Metrics collection: Daily at 18:00")

    while True:
        schedule.run_pending()
        time.sleep(60)

    if __name__=="__main__":
        main()
