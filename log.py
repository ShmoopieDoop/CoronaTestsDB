import logging

logger = logging.getLogger(__name__)
f_handler = logging.FileHandler("DB.log")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.info("started logging")
