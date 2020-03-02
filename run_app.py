# -*- coding: utf-8 -*-
"""
description:
"""

from aiohttp import web

from app import create_app
from app import WorkerSettings


application = create_app()

if __name__ == '__main__':
    web.run_app(application)
