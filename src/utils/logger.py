import logging
import csv
from datetime import datetime
from pathlib import Path
from Config import Config


class ActivityCSVHandler(logging.Handler):
    """
    A logging handler that appends a CSV row for every LogRecord.
    Columns: Timestamp, LoggerName, Level, Message
    """
    def __init__(self, csv_path, level=logging.INFO):
        super().__init__(level)
        self.csv_path = Path(csv_path)
        # ensure parent directory exists
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record):
        try:
            row = [
                datetime.now().isoformat(),
                record.name,
                record.levelname,
                self.format(record)  # formatted message (includes extra info if formatter set)
            ]
            file_exists = self.csv_path.exists()
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Logger", "Level", "Message"])
                writer.writerow(row)
        except Exception:
            # ensure logging errors don't break the app
            self.handleError(record)






def setup_logger():
    #setting up application logger
    Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    #fILE HANDLER
    fh = logging.FileHandler(Config.LOG_FILE)
    fh.setLevel(logging.DEBUG)

    #Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)


    # CSV activity handler
    csv_handler = ActivityCSVHandler(Config.ACTIVITY_LOG, level=logging.INFO)
    csv_handler.setLevel(logging.INFO)



    #Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    csv_handler.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(csv_handler)

    return logger

def log_activity(activity_type, status, details):
    #Logging activity type to CSV file
    log_file = Config.ACTIVITY_LOG
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_exists = log_file.exists()

    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not log_exists:
            writer.writerow(['Timestamp', 'Type', 'Status', 'Details'])
            
        writer.writerow([
            datetime.now().isoformat(),
            activity_type,
            status,
            details
        ])

logger = setup_logger()