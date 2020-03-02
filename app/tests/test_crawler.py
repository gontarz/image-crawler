# -*- coding: utf-8 -*-
"""
description:
"""
import unittest
import os

from bs4 import BeautifulSoup

from app.crawler import visible, extract_images_links, extract_text
from app.settings import BASE_DIR


class TestCrawler(unittest.TestCase):
    def test_visible(self):
        """
        in test_crawler.html all visible text contains 't' and non-visible 'f'
        """
        with open(os.path.join(BASE_DIR, 'app/tests/test_html/test_crawler.html')) as html:
            soup = BeautifulSoup(html, 'html.parser')

        data = soup.findAll(text=True)
        result = {text.strip() for text in filter(visible, data) if text.strip()}
        self.assertEqual({'t'}, result)

        result = [elem for elem in data if visible(elem)]
        self.assertTrue(all(result))


class TestCrawlerAsync(unittest.IsolatedAsyncioTestCase):
    async def test_extract_text(self):
        with open(os.path.join(BASE_DIR, 'app/tests/test_html/example..html')) as html:
            crawled = await extract_text(html)
        expected = '''Example Domain
This domain is for use in illustrative examples in documents. You may use this
        domain in literature without prior coordination or asking for permission.
More information...'''
        self.assertEqual(expected, crawled)

    async def test_extract_images_links(self):
        with open(os.path.join(BASE_DIR, 'app/tests/test_html/test_crawler.html')) as html:
            crawled = await extract_images_links(html)
        expected = {'test1', 'test2', 'test3'}
        self.assertEqual(expected, crawled)


if __name__ == '__main__':
    unittest.main()
