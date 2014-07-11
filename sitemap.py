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
       - It parses a page and contains page data
    '''

    processed_urls = []
    processed_pages = []

    def __init__(self, url):
        self.url = url
        self.nested = []
        self.connected_to = []
        self.processed = False

    def process(self):
        self.__process_url(self.url)
        self.processed = True

    @staticmethod
    def GetPage(url):
        processed_page = list([page.url == url for page in Page.processed_pages])
        if len(processed_page) > 1:
            return processed_page[0]
        else:
            page = Page(url)
            return page


    def __process_url(self, url):
        print url
        page = Page.GetPage(url)
        if page.processed:
            raise Exception('The page should not be processed before. Logical error.')

        nested_urls = self.__get_urls(url)
        for nested_url in nested_urls:
            if not url.startswith('/'):
                continue
            page = Page.GetPage(nested_url)
            print page
            page.connected_to.append(self)
            self.nested.append(page)
            self.processed_pages.append((url, page))

            page.process()

    def __get_urls(self, url):
        html = urllib2.urlopen(url).read()
        urls = re.findall(r'<a\s{1,3}href=[\'"]?([^\'" >]+)', html)
        return urls


page = Page.GetPage(domain_name)
page.process()

print options, args