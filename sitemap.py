__author__ = 'viktor'

from optparse import OptionParser
from page import Page

MAX_DEPTH = 10

parser = OptionParser()
parser.add_option('-o', '--output-csv', dest='filename', help='It writes the report to a file')
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

Page.domain_name = domain_name
page = Page.GetPage('/', 'Home')
page.process()

if  options.filename:
    page.SaveTable(options.filename)
else:
    print page