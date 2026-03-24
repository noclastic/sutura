import logging
import os

LOG_FILE = os.path.join(os.path.expanduser("~"), ".sutura_errors.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Sutura")

def get_log_file_path():
    return LOG_FILE
