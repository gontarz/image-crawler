# -*- coding: utf-8 -*-
"""
description: simple views
"""

import logging

from aiohttp import web

from app.task_queue import check_task_status
from app.models import URL
from app.utlis import extended_dump

logger = logging.getLogger(__name__)


def internal_error_response(error):
    response_body = {'status': 'failed', 'reason': str(error)}
    logger.error(error)
    return web.json_response(data=response_body, status=500)


def success_response(job_id):
    return {
        'status': 'success',
        'task_id': f'{job_id}'
    }


async def get_task_status(request):
    try:
        task_id = request.match_info.get('task_id')
        status = await check_task_status(
            task_id=task_id,
            redis=request.app['arq_redis']
        )
        return web.json_response(data={'status': f'{status}'}, status=200)

    except Exception as e:
        return internal_error_response(e)


async def get_receive(request):
    try:
        request_body = await request.json()
        url = request_body['url']
        # logger.error(url)
        data = URL.as_dict(url)
        # logger.error(data)

        return web.json_response(data=data, status=200, dumps=extended_dump)

    except Exception as e:
        return internal_error_response(e)


async def post_crawl_images(request):
    try:
        request_body = await request.json()
        url = request_body['url']

        redis = request.app['arq_redis']
        job = await redis.enqueue_job('fetch_images', url)
        data = success_response(job.job_id)

        return web.json_response(data=data, status=201)

    except Exception as e:
        return internal_error_response(e)


async def post_crawl_text(request):
    try:
        request_body = await request.json()
        url = request_body['url']

        redis = request.app['arq_redis']
        job = await redis.enqueue_job('fetch_text', url)
        data = success_response(job.job_id)

        return web.json_response(data=data, status=201)

    except Exception as e:
        return internal_error_response(e)
