import pytz
import logging
import datetime

def get_logging(log_dir):
    """Get logging function

    Args:
        log_dir (String): location directory (relative path)

    Returns:
        logging: custom logging
    """
    
    logging.Formatter.converter = logging.Formatter.converter = lambda *args: datetime.datetime.now(tz=pytz.timezone('Asia/Ho_Chi_Minh')).timetuple()
    logging.basicConfig(filename=log_dir, level=logging.INFO, format = '[%(asctime)s] - [%(levelname)s] - [%(funcName)s] - [%(lineno)d] - %(message)s',
                    filemode="w")
    return logging