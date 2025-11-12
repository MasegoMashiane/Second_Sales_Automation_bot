import logging
import csv
from datetime import datetime
from pathlib import Path
from config import Config

def setup_logger():
    #setting up application logger
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger('automation')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    #fILE HANDLER
    fh = logging.FileHandler(Config.load_file)
    fh.setLevel(logging.DEBUG)

    #Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    #Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def log_activity(activity_type, status, details):
    #Logging activity type to CSV file
    log_file = Config.ACTIVITY_LOG
    log_exists = log_file.exists()

    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(['Timestamp', 'Type', 'Status', 'Details'])
        writer.writerow([
            datetime.now().isoformat,
            activity_type,
            status,
            details
        ])

logger = setup_logger