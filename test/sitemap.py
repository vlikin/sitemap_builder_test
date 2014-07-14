__author__ = 'viktor'

import os
import unittest

from lib.sitemap import Sitemap


class TestSitemap(unittest.TestCase):

    def setUp(self):
        self.domain_name = 'file://' + os.path.abspath(os.path.dirname(__file__) + '/test_data')
        self.index_file = '/index.html'
        self.sitemap = Sitemap(self.domain_name)

    def test_get_urls(self):
        urls = self.sitemap._get_urls(self.index_file)
        self.assertEqual(urls[0], '/')
        self.assertEqual(urls[1], '/about_us.html')
        self.assertEqual(urls[2], '/contacts.html')
        self.assertEqual(urls[3], '/wiki.html')

if __name__ == '__main__':
    unittest.main()