import logging
import sys
import os
from datetime import datetime

def setup_logger(name="BLCKScopezBot", log_dir="./logs", level=logging.INFO):
    # create directory if not exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # create filenames with dates
    date_str = datetime.now().strftime("%d-%m-%Y")
    log_file = os.path.join(log_dir, f"{date_str}-bot.log")
    
    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    
    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # file handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()