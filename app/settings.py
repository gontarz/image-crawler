# -*- coding: utf-8 -*-
"""
description: applications settings
"""

import os

from arq.connections import RedisSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_CONFIG = {
    'host': 'postgres',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'postgres'
}
DB_URI = 'postgres://postgres:postgres@postgres/postgres'

REDIS_HOST = 'redis'
REDIS_PORT = 6379

ARQ_REDIS_SETTINGS = RedisSettings(
    host=REDIS_HOST,
    port=REDIS_PORT
)

IMAGES_DIR = 'images'
IMAGES_DIR_PATH = os.path.join(BASE_DIR, IMAGES_DIR)

LOG_DIR = 'logs'
LOG_DIR_PATH = os.path.join(BASE_DIR, LOG_DIR)

LOGGING_LEVEL = 'DEBUG'

LOGGING_CONFIG = {
    'version': 1,
    # 'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
        },
        'error': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'mode': 'a',
            'maxBytes': 1024 ** 2,
            'backupCount': 10
        },
        'api_rotating_file_handler': {
            'level': LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'api.log'),
            'mode': 'a',
            'maxBytes': 1024 ** 2,
            'backupCount': 10
        },
        'crawler_rotating_file_handler': {
            'level': LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'crawler.log'),
            'mode': 'a',
            'maxBytes': 1024 ** 2,
            'backupCount': 10
        },
        'task_queue_rotating_file_handler': {
            'level': LOGGING_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'task_queue.log'),
            'mode': 'a',
            'maxBytes': 1024 ** 2,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'info_rotating_file_handler', 'error_file_handler'],
            'level': 'NOTSET',
        },
        'run_app': {
            'handlers': ['console', 'info_rotating_file_handler', 'error_file_handler'],
            'level': LOGGING_LEVEL,
            'propagate': False
        },
        'app.api': {
            'handlers': ['console', 'api_rotating_file_handler', 'error_file_handler'],
            'level': LOGGING_LEVEL,
            'propagate': False
        },
        'app.crawler': {
            'handlers': ['console', 'crawler_rotating_file_handler', 'error_file_handler'],
            'level': LOGGING_LEVEL,
            'propagate': False
        },
        'app.task_queue': {
            'handlers': ['console', 'task_queue_rotating_file_handler', 'error_file_handler'],
            'level': LOGGING_LEVEL,
            'propagate': False
        }
    }
}
