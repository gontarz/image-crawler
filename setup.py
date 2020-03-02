# -*- coding: utf-8 -*-
"""
description:
"""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.0.1'

install_requires = [
    # webapp
    'aiohttp==3.6.2',

    # crawler
    'beautifulsoup4==4.8.2',

    # task queue
    'aioredis==1.3.1',
    'arq==0.18.4',

    # db
    'sqlalchemy==1.3.13',
    'aiopg==1.0.0',
    'alembic==1.4.0',

    # server
    'gunicorn==20.0.4',
]

setup(
    name='image-crawler',
    version=version,
    author_email="python.backend.dev@gmail.com",
    description='small asynchronous images and text web crawler',
    long_description=long_description,
    ulr='https://github.com/kotEustachy/image-crawler',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    # extras_require={
    #     'dev': [
    #         'pytest',
    #         'pytest-pep8',
    #         'pytest-cov'
    #     ]
    # },
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
