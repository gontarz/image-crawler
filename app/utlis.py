# -*- coding: utf-8 -*-
"""
description:
"""

import json
from uuid import UUID
from datetime import datetime


def extended_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)


def extended_dump(data):
    """
    extended json dump for sqlalchemy and aiohttp json_response
    :param data: data to dump
    :return: dumped data
    """
    return json.dumps(data, default=extended_encoder)
