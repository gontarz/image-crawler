# -*- coding: utf-8 -*-
"""
description:
"""

import unittest
import os
from hashlib import md5

from aiohttp import ClientSession
from arq import create_pool
from arq.connections import RedisSettings

from app.task_queue import validate_image, fetch_text
from app.settings import BASE_DIR, IMAGES_DIR_PATH


class TestQueue(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # self.redis = await create_pool(RedisSettings())
        self.queue_ctx = dict()
        self.queue_ctx['session'] = ClientSession()

    async def asyncTearDown(self):
        await self.queue_ctx['session'].close()

    async def test_validate_image(self):
        img_path = os.path.join(BASE_DIR, 'app/tests/test_img/test.jpeg')
        with open(img_path, 'rb') as f:
            raw = f.read()
        result = await validate_image(raw)
        img_md5 = md5(raw).hexdigest()

        hashed_path = os.path.join(IMAGES_DIR_PATH, img_md5)
        self.assertEqual(hashed_path, result)

        false_result = await validate_image(b'123')
        self.assertFalse(false_result)

    async def test_fetch_images(self):
        # os.path.join(BASE_DIR, 'app/tests/test_img/test.jpeg')
        #
        # url = 'file:///'
        # await fetch_images(self.queue_ctx, url)
        pass

    async def test_fetch_text(self):
        url = 'http://example.com/'
        crawled = await fetch_text(self.queue_ctx, url)
        expected = '''Example Domain
        This domain is for use in illustrative examples in documents. You may use this
                domain in literature without prior coordination or asking for permission.
        More information...'''

        self.assertEqual(expected, crawled)

    #
    # async def on_cleanup(self):
    #     events.append("cleanup")
    # async def main():
    #     redis = await create_pool(RedisSettings())
    #     for url in (
    #             # 'https://facebook.com',
    #             # 'https://microsoft.com',
    #             'https://github.com',
    #             # 'http://example.com/',
    #     ):
    #         # await redis.enqueue_job('download_content', url)
    #         await redis.enqueue_job('download_images', url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
