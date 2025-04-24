import logging
from logging.handlers import RotatingFileHandler

def configure_loggers(prefix: str = ""):
    logging.getLogger('').setLevel(logging.INFO)
    try:
        rotatingHandler = RotatingFileHandler(filename=f"/logs/{prefix}_rotating.log", maxBytes=4096*8, backupCount=2)
    except:
        rotatingHandler = RotatingFileHandler(filename=f"./{prefix}_rotating.log", maxBytes=4096*8, backupCount=2)
    rotatingHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotatingHandler.setFormatter(formatter)
    logging.getLogger('').addHandler(rotatingHandler)