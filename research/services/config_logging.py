import logging
import os
class Log():
    def __init__(self):
        self.path = f'research/logs/'
        self.file = f'log.log'

    def locate(self):
        try:
            # and os.path.isfile(f'{self.file}.log')
 
            # Check if the path already exists.
            if os.path.exists(self.path):
                pass
    
            else:
                os.makedirs(self.path)
                # Create folder
 
        except Exception as error:
            self.logger.error('Error organizing file log. ' + error)

    def logger(self, name):
        try:
            self.locate()
            logging.basicConfig(filename=f'{self.path}{self.file}',
                                level=logging.INFO,
                                format='%(asctime)s %(levelname)s %(name)s %(message)s')
            logger = logging.getLogger(name)
            
            return logger
        except Exception as error:
            print('Error log ' + error)

