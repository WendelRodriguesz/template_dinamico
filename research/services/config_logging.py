import logging


def log(name):
    try:
        logging.basicConfig(filename='research/log.log',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(name)
        
        return logger
    except:
        pass