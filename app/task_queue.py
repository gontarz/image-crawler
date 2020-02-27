# -*- coding: utf-8 -*-
"""
description: arq queue with helper functions
"""

import asyncio
import logging
import os
from imghdr import what as what_img
from hashlib import md5

from aiohttp import ClientSession
from arq.jobs import Job

from app.crawler import extract_text, extract_images_links
from app.settings import IMAGES_DIR_PATH, ARQ_REDIS_SETTINGS
from app.models import URL

logger = logging.getLogger(__name__)


async def check_task_status(task_id, redis):
    """Return status from arq queue"""
    return await Job(job_id=task_id, redis=redis).status()


async def validate_image(raw_data):
    """check image type and existence in filesystem"""
    if what_img('', raw_data):
        img_md5 = md5(raw_data).hexdigest()
        image_path = f'{IMAGES_DIR_PATH}/{img_md5}'

        if not os.path.exists(image_path):
            return image_path


async def fetch_image(session, url):
    async with session.get(url) as response:
        raw = await response.read()

    if image_path := await validate_image(raw):
        logger.debug(f'Image validated {url}')
        with open(image_path, "wb") as file:
            file.write(raw)
        logger.debug(f'Image saved to storage {url}')

        return dict(
            name=url.split('/')[-1],
            md5=image_path.split('/')[-1]
        )


async def fetch_images(ctx, url):
    logger.debug(f'Fetch images from {url}')
    session = ctx['session']

    async with session.get(url) as response:
        content = await response.text()

    images_urls = await extract_images_links(content)
    logger.debug(f'Images to fetch  {images_urls}')

    done, pending = await asyncio.wait([
        fetch_image(session, url)
        for url in images_urls
    ])
    images_result = [task.result() for task in done if task.result()]
    logger.debug(f'Fetched images {images_result}')

    if images_result:
        logger.debug(f'Try to insert images data from {url}')
        URL.save_images(url, images_result)
        logger.debug(f'Images data commited from url {url}')


async def fetch_text(ctx, url):
    session = ctx['session']

    async with session.get(url) as response:
        content = await response.text()

    text = await extract_text(content)
    logger.debug(f'{text} text')

    if text:
        logger.debug(f'Try to insert text data from {url}')
        URL.save_text(url, text)
        logger.debug(f'Text data commited from url {url}')


async def on_startup(ctx):
    # aiohttp session
    ctx['session'] = ClientSession()

    logger.info(f'arq-worker startup initiated')


async def on_shutdown(ctx):
    # aiohttp session
    await ctx['session'].close()

    logger.info(f'arq-worker shutdown')


# WorkerSettings defines the settings to use when creating the work, it's used by the arq cli
class WorkerSettings:
    functions = [
        fetch_text,
        fetch_images
    ]
    on_startup = on_startup
    on_shutdown = on_shutdown
    redis_settings = ARQ_REDIS_SETTINGS
