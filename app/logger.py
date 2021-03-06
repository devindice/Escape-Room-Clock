import logging as log
from logging.config import dictConfig
import pathlib
import os

# Usage
# import app.logger as logger
# logger.log.debug('This is a debug message')
# logger.log.info('This is an info message')
# logger.log.warning('This is a warning message')
# logger.log.error('This is an error message')
# logger.log.critical('This is a critical message')

appPath = str(pathlib.Path(__file__).parent.resolve()).removesuffix('app')

LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': [
                'console_handler_stream',
            	'console_handler_file',
            	'error_handler_file',
                'debug_handler_file',
            ],
            'propagate': False,
        },
    },
    'handlers': {
        'console_handler_stream': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'console_handler_file': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': 'logs/console.log',
            'mode': 'a',
        },
        'error_handler_file': {
            'level': 'WARNING',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'a',
        },
        'debug_handler_file': {
            'level': 'DEBUG',
            'formatter': 'debug',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'mode': 'a',
        }
    },
    'formatters': {

        'default': {
            'format': '%(asctime)s %(levelname)s - %(module)s - %(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'
        },
        'debug': {
            'format': '%(asctime)s PID: %(process)d Lvl: %(levelname)s Module: %(module)s Ln#: %(lineno)s Message: %(message)s'
        },
    },
}

LOGGING_CONFIG['handlers']['console_handler_file']['filename'] = appPath + 'logs/console.log'
LOGGING_CONFIG['handlers']['error_handler_file']['filename'] = appPath + 'logs/error.log'
LOGGING_CONFIG['handlers']['debug_handler_file']['filename'] = appPath + 'logs/debug.log'

print(LOGGING_CONFIG)

isExist = os.path.exists(appPath + 'logs')
if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs(appPath + 'logs')

dictConfig(LOGGING_CONFIG)

