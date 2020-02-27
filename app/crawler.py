# -*- coding: utf-8 -*-
"""
description: crawler functions to extract visible text and images links
"""

import re

from bs4 import BeautifulSoup


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


async def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll(text=True)

    return '\n'.join([text.strip() for text in filter(visible, data) if text.strip()])


async def extract_images_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    image_tags = soup.findAll('img')
    images_links = set([image_tag.get('src') for image_tag in image_tags if image_tag.get('src')])
    return images_links
