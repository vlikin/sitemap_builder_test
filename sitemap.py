__author__ = 'viktor'
from optparse import OptionParser
import urllib2
import re
import urlparse
import pprint

MAX_DEPTH = 10
MAX_LEVEL = 100

parser = OptionParser()
parser.add_option('-o', '--output-cvs', dest='filename', help='It writes the report to a file')
parser.add_option('-d', '--depth', dest='depth', default=3, help='It defines a depth to go into.')
(options, args) = parser.parse_args()

if len(args) == 0:
    print 'The process is broken. A domain name is not set'
    exit()

domain_name = args[-1]
if int(options.depth) > MAX_DEPTH:
    print 'The process is broken. The max depth is - %d' % MAX_DEPTH
    exit()

print 'The script starts to parse the domain name - %s' % domain_name

class Page(object):
    '''
       - It parses a page and contains page data
    '''

    processed_urls = []
    processed_pages = []
    domain_name = ''

    def __init__(self, url, title, level=0):
        self.url = url
        self.title = ''
        self.nested = []
        self.connected_to = []
        self.processed = False
        self.level = level

    def process(self):
        if self.processed or self.level > 3:
            print 'break'
            return False
        print 'process - %s' % self.url
        self.__process_url(self.url)

    @staticmethod
    def GetPage(url, title='', level=0):
        processed_page = [page for page in Page.processed_pages if page.url == url]
        print processed_page
        if len(processed_page) > 0:
            return processed_page[0]
        else:
            print 'new page - %s' % url
            page = Page(url, title, level)
            return page


    def __process_url(self, url):
        nested_urls = self.__get_urls(url)
        for nested_url in nested_urls:
            if not nested_url[0].startswith('/'):
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
        print 'load - %s' % relative_url
        html = urllib2.urlopen(url).read()
        urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)[\'"]>?([^<]+)', html)
        return urls

    def __str__(self):
        str = '%s - %s'

#domain_name = 'http://dsaua.org/'
Page.domain_name = domain_name
page = Page.GetPage('/', 'Home')
page.process()

print options, args

content = '<a href="link">Text</a> fasd asdf <a href="link1">Text1</a> fasd asdf as <a href="link2">Text2</a>'