import logging
from logging import StreamHandler, Formatter
from logging import FileHandler
from logging.handlers import RotatingFileHandler

log_name = 'petrol_filter.log'

logging.basicConfig(filename=log_name, level=logging.DEBUG)

logger = logging.getLogger('petrol_filter.logger')
logger.addHandler(StreamHandler())

log_file = RotatingFileHandler(
    log_name,
    maxBytes=1024 * 1024,
    backupCount=3
)
log_file.setFormatter(Formatter('%(asctime)s: %(message)s'))
logger.addHandler(log_file)

def log_info(s=None):
    logger.info(s)

def log_debug(s):
    logger.debug(s)


def log_error(s):
    logger.error(s)

def log_error1(s):
    logger.error1(s)


def log_error2(s):
    logger.error2(s)