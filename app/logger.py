import logging as log
from logging.config import dictConfig
import os

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
            'level': 'ERROR',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'a',
        }
    },
    'formatters': {

        'console': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'debug': {
            'format': '%(asctime)s - %(levelname)s - %(process)d - %(module)s|%(lineno)s - %(message)s'
        },
        'error': {
            'format': '%(asctime)s - %(levelname)s - %(process)d - %(module)s|%(lineno)s - %(message)s'
        },
    },
}

isExist = os.path.exists('logs')
if not isExist:
  
  # Create a new directory because it does not exist 
  os.makedirs('logs')

dictConfig(LOGGING_CONFIG)

