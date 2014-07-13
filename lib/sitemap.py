__author__ = 'viktor'

from page import Page

import logging
import re
import urllib2
import urlparse


# noinspection PyBroadException
class Sitemap(object):

    def __init__(self, domain_name, max_depth=3):
        self.processed_pages = []
        self.domain_name = domain_name
        self.max_depth = max_depth

    def get_page(self, url):
        """
            - It creates or returns already an initialized page object.
        """
        processed_page = [page for page in self.processed_pages if page.url == url]
        if len(processed_page) > 0:
            return processed_page[0]
        else:
            page = Page(url)
            return page

    def process(self, url):
        page = self.get_page(url)
        self.__process_page(page)
        return page

    def __process_page(self, page, level=0):
        """
            - It processes a page by the url.
        """
        if page.processed or level > self.max_depth:
            return

        nested_urls = self.__get_urls(page.url)
        for nested_url in nested_urls:
            if not nested_url.startswith('/') or nested_url.strip() == '' or nested_url.startswith('//'):
                continue
            nested_page = self.get_page(nested_url)
            if nested_page.processed:
                nested_page.connected_to.append(page)
            else:
                nested_page.connected_to.append(page)
                page.nested.append(nested_page)
                self.processed_pages.append(nested_page)
        page.processed = True

        for nested_page in page.nested:
            self.__process_page(nested_page, level + 1)

    def __get_urls(self, relative_url):
        """
            - It loads a page and extracts urls from.
        """
        try:
            url = urlparse.urljoin(self.domain_name, relative_url)
            html = urllib2.urlopen(url).read()
            urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)[\'"][^>]*>?([^<]+)', html)
            return set([url[0] for url in urls])

        except:
            logging.exception('Parsing the url - %s failed.')
            return []
