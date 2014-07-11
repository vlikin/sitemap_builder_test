__author__ = 'viktor'

import csv
import re
import urllib2
import urlparse

class Page(object):
    '''
       - It parses a page and contains page data
    '''

    processed_pages = []
    domain_name = ''
    max_depth = 3

    def __init__(self, url):
        self.url = url
        self.nested = []
        self.connected_to = []
        self.processed = False

    def process(self, level=0):
        '''
            - It initializes the parsing process.
        '''
        if self.processed:
            return
        if (level > Page.max_depth):
            return
        self.__process_url(self.url, level)

    @staticmethod
    def GetPage(url):
        '''
            - It creates or returns already an initialized page object.
        '''
        processed_page = [page for page in Page.processed_pages if page.url == url]
        if len(processed_page) > 0:
            return processed_page[0]
        else:
            page = Page(url)
            return page

    def __process_url(self, url, level=0):
        '''
            - It processes a page by the url.
        '''
        nested_urls = self.__get_urls(url)
        for nested_url in nested_urls:
            if not nested_url.startswith('/') or nested_url.strip() == '' or nested_url.startswith('//'):
                continue
            page = Page.GetPage(nested_url)
            if page.processed:
                page.connected_to.append(self)
            else:
                page.connected_to.append(self)
                self.nested.append(page)
                self.processed_pages.append(page)
        self.processed = True

        for page in self.nested:
            page.process(level + 1)

    def __get_urls(self, relative_url):
        '''
            - It loads a page and extracts urls from.
        '''
        try:
            url = urlparse.urljoin(self.domain_name, relative_url)
            html = urllib2.urlopen(url).read()
            urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)[\'"][^>]*>?([^<]+)', html)
            return list([url[0] for url in urls])

        except:
            return []

        return url_list

    def to_string(self, level=0):
        '''
            - It represents the object in the string format.
        '''
        if level > Page.max_depth:
            return
        str = '%d %s %s\n' % (self.level, '--' * self.level, self.url)
        print str
        for page in self.nested:
            str = '%s%s' % (str, self.to_string(level + 1))

        return str

    def GetTable(self, parent=None, level=0):
        '''
            - It goes through the relation tree and build the table.
        '''
        if level > Page.max_depth:
            return []
        if parent == None:
            parent = self
        row_list = []
        row = [id(self), level, self.url, id(parent)]
        row_list.append(row)
        for page in self.nested:
            row_list.extend(page.GetTable(self, level+1))

        return row_list

    def SaveTable(self, filename):
        '''
            - It saves the processed table to a file.
        '''
        table = self.GetTable()
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in table:
                writer.writerow(row)