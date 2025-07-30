import logging
import os

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logger = logging.getLogger("osint_tool")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("logs/osint_tool.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger

logger = setup_logger()
