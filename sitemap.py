__author__ = 'viktor'

from lib.sitemap import Sitemap
import logging
from optparse import OptionParser
import sys


MAX_DEPTH = 10

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# It defines console parameters.
parser = OptionParser()
parser.add_option('-o', '--output-csv', dest='filename', help='It writes the report to a file')
parser.add_option('-d', '--depth', dest='depth', default=3, help='It defines a depth to go into.')
(options, args) = parser.parse_args()

# It validates options.
if len(args) == 0:
    logging.info('The process is broken. A domain name is not set')
    exit()

domain_name = args[-1]
if int(options.depth) > MAX_DEPTH:
    logging.info('The process is broken. The max depth is - %d' % MAX_DEPTH)
    exit()

# It starts the validation process.
logging.info('The script starts to parse the domain name - %s' % domain_name)
sitemap = Sitemap(domain_name, int(options.depth))

page = sitemap.process('/')

logging.info('The site has been parsed successfully.')

# if a file is not define it outputs data to the screen.
if options.filename:
    page.save_table(options.filename, int(options.depth))
    logging.info('Results are saved to - %s' % options.filename)
else:
    logging.info(page.to_string(int(options.depth)))

logging.info('The process is finished.')