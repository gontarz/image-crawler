# -*- coding: utf-8 -*-
"""
description:
"""

import logging
from logging.config import dictConfig

from aiohttp import web

from app import create_app
from app.task_queue import WorkerSettings
from app.settings import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

application = create_app()

if __name__ == '__main__':
    web.run_app(application)
