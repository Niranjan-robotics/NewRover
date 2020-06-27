import time
import logging
import logging.config
import yaml


# with open('/home/pi/projects/NewRover/config.yaml', 'r') as f:
    # config = yaml.safe_load(f.read())
    # logging.config.dictConfig(config)

logging.basicConfig(filename='/home/pi/projects/NewRover/consoleLog.log', filemode='w',level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def logInfo(msg):
    global logger
    logger.info(msg)
