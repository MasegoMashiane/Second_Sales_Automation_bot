import schedule
import logging
import time
from main import run_social, run_sales, collect_metrics
from src.utils.logger import logger

def main():
    #setup and run scheduler

    #schedule tasks
    schedule.every().day.at("09:00").do(run_sales)
    schedule.every(30).minutes.do(run_social)
    schedule.every().day.at("18:00").do(collect_metrics)

    logging.info("Automation Scheduler Started")
    logging.info("="*50)
    logging.info("Sales campaigns: Daily at 09:00")
    logging.info("Social posts: Every 30 minutes")
    logging.info("Metrics collection: Daily at 18:00")

    while True:
        schedule.run_pending()
        time.sleep(60)

    if __name__=="__main__":
        main()
