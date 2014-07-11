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

    def __init__(self, url, title, level=0):
        self.url = url
        self.title = title
        self.nested = []
        self.connected_to = []
        self.processed = False
        self.level = level

    def process(self):
        if self.processed or self.level > 5:
            print 'break'
            return False
        self.__process_url(self.url)

    @staticmethod
    def GetPage(url, title='', level=0):
        processed_page = [page for page in Page.processed_pages if page.url == url]
        if len(processed_page) > 0:
            return processed_page[0]
        else:
            page = Page(url, title, level)
            return page


    def __process_url(self, url):
        nested_urls = self.__get_urls(url)
        for nested_url in nested_urls:
            if not nested_url[0].startswith('/') or nested_url[0].strip() == '':
                continue
            page = Page.GetPage(nested_url[0], nested_url[1], self.level + 1)
            if page.processed:
                page.connected_to.append(self)
            else:
                page.connected_to.append(self)
                self.nested.append(page)
                self.processed_pages.append(page)
        self.processed = True
        for page in self.nested:
            page.process

    def __get_urls(self, relative_url):
        url = urlparse.urljoin(self.domain_name, relative_url)
        html = urllib2.urlopen(url).read()
        urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)[\'"][^>]*>?([^<]+)', html)
        url_list = []
        for url in urls:
            url_list.append([url[0], re.sub(r'<[^>]*>', '', url[1])])

        return url_list

    def __str__(self):
        str = '%d %s %s\n' % (self.level, '--' * self.level, self.url)
        for page in self.nested:
            str = '%s%s' % (str, page.__str__())

        return str

    def GetTable(self, parent=None):
        if parent == None:
            parent = self

        row_list = []
        row = [id(self), self.level, self.url, id(parent)]
        row_list.append(row)
        for page in self.nested:
            row_list.extend(page.GetTable(self))

        return row_list

    def SaveTable(self, filename):
        table = self.GetTable()
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in table:
                writer.writerow(row)
