import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s %(message)s'
        }
    },
   'handlers' : {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
   },
   'loggers': {
        '__main__': {
            'handlers' : ['default'],
            'level': 'WARNING',
            'propagate': False,
        },
   },
   'root': {
        'level': 'INFO',
        'handlers': ['default']
   },
})
