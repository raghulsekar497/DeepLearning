# logger.py
import logging
import os
from datetime import datetime

def create_logger(video_type, video_name):
    os.makedirs("static/logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log_{video_type}_{timestamp}.log"
    log_path = os.path.join("static/logs", log_filename)

    logger = logging.getLogger(log_filename)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info(f"Started tracking | Type: {video_type}, Video: {video_name}")
    return logger
