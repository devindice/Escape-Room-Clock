import logging as log
from logging.config import dictConfig
import os

# Usage
# import app.logger as logger
# logger.log.debug('This is a debug message')
# logger.log.info('This is an info message')
# logger.log.warning('This is a warning message')
# logger.log.error('This is an error message')
# logger.log.critical('This is a critical message')

LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': [
            	'console_stream_handler',
            	'console_file_handler',
            	'debug_file_handler',
            	'error_file_handler',
            ],
            'propagate': False,
        },
    },
    'handlers': {
        'console_stream_handler': {
            'level': 'INFO',
            'formatter': 'console',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'console_file_handler': {
            'level': 'INFO',
            'formatter': 'console',
            'class': 'logging.FileHandler',
            'filename': 'logs/console.log',
            'mode': 'a',
        },
        'debug_file_handler': {
            'level': 'DEBUG',
            'formatter': 'debug',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'mode': 'a',
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'a',
        }
    },
    'formatters': {

        'console': {
            'format': '%(asctime)s %(levelname)s - %(module)s - %(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'
        },
        'debug': {
            'format': '%(asctime)s PID: %(process)d Lvl: %(levelname)s Module: %(module)s Ln#: %(lineno)s Message: %(message)s'
        },
        'error': {
            'format': '%(asctime)s %(levelname)s - %(module)s - %(message)s',
            'datefmt':'%Y-%m-%d %H:%M:%S'
        },
    },
}

isExist = os.path.exists('logs')
if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs('logs')

dictConfig(LOGGING_CONFIG)

