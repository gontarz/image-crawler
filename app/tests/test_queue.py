# -*- coding: utf-8 -*-
"""
description:
"""

from arq import create_pool
from arq.connections import RedisSettings


async def main():
    redis = await create_pool(RedisSettings())
    for url in (
            # 'https://facebook.com',
            # 'https://microsoft.com',
            'https://github.com',
            # 'http://example.com/',
    ):
        # await redis.enqueue_job('download_content', url)
        await redis.enqueue_job('download_images', url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
