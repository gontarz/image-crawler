# -*- coding: utf-8 -*-
"""
description: app factory with routing
"""
import logging

from aiohttp import web
from arq import create_pool

from app.views import (
    get_task_status,
    get_receive,
    post_crawl_images,
    post_crawl_text
)
from app.settings import ARQ_REDIS_SETTINGS

logger = logging.getLogger(__name__)


async def arq_redis_startup(app):
    """
    signal to create Redis pool
    """
    app['arq_redis'] = await create_pool(ARQ_REDIS_SETTINGS)
    logger.info(f'arq-redis pool created')


async def arq_redis_cleanup(app):
    """
        signal to close Redis pool
    """
    app['arq_redis'].close()
    await app['arq_redis'].wait_closed()
    logger.info(f'arq-redis pool closed')


def create_app():
    app = web.Application()

    routes = [
        web.post('/crawl/text/', post_crawl_text),
        web.post('/crawl/images/', post_crawl_images),
        web.get('/task-status/{task_id}/', get_task_status),
        web.get('/receive/', get_receive)

    ]

    app.add_routes(routes)
    app.on_startup.extend([
        arq_redis_startup
    ])
    app.on_cleanup.extend([
        arq_redis_cleanup
    ])

    return app


if __name__ == '__main__':
    web.run_app(create_app())
