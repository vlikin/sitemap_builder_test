__author__ = 'viktor'
from optparse import OptionParser
import urllib2
import re

MAX_DEPTH = 10

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
        It parses a page and contains page data
    '''

    processed_urls = []
    processed_pages = []

    def __init__(self, page_url):
        self.page_url = page_url
        self.nested_pages = []

    def process(self):
        self.__process_url(self.page_url)

    def __process_url(self, url):
        if url in self.processed_urls:
            return True
        self.processed_urls.append(url)

        urls = self.__get_urls(url)
        for url in urls:
            if url.startswith('/'):
                print url


class Sitemap(object):
    '''
        - It builds a sitemap by an url.
    '''

    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.processed_urls = []

    def start(self):
        self.__process_url(self.domain_name)

    def __process_url(self, url):
        if url in self.processed_urls:
            return True
        self.processed_urls
        urls = self.__get_urls(url)
        for url in urls:
            if url.startswith('/'):
                print url


    def __get_urls(self, url):
        html = urllib2.urlopen(domain_name).read()
        urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)', html)
        return urls

sitemap_builder = Sitemap(domain_name)
sitemap_builder.start()
print options, args