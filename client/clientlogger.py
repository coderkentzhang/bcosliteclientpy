from client_config import client_config
import logging
from logging import handlers
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
logfile=client_config.logdir+"/client.log"
#handler = logging.FileHandler(logfile)
handler = logging.handlers.TimedRotatingFileHandler(logfile, 'D', 1, 0) #切割日志
handler.suffix = '%Y%m%d' #切割后的日志设置后缀
#handler.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)