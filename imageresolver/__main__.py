from __future__ import print_function
import sys
import logging
import time
from optparse import OptionParser
from imageresolver import *

logger = logging.getLogger('ImageResolver')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

opts = OptionParser()
opts.add_option("-u", "--url", dest="url", help="A url to parse")
opts.add_option("-d", "--debug", action="store_true", dest="debug", help="enable debugging")
opts.add_option("-r", "--max-read", dest="max_read", help="Set the max read size")
opts.add_option("-c", "--chunk-size", dest="chunk_size", help="Chunk size to read on each pass")
opts.add_option("-a", "--read-all", dest="read_all",
                help="Read the entire image before checking size. Useful for some JPGs. Overrides --max-read")
opts.add_option("-b", "--adblock", action="store_true", dest="use_adblock_filters", help="Use adblock filters.")
opts.add_option("-s", "--no-ruleset", action="store_true", dest="use_js_ruleset",
                help="Use a custom ruleset for scoring.")
opts.add_option("--benchmark", action="store_true", dest="benchmark",
                help="Benchmark the total time it takes for the script to return an image")
opts.add_option("-n", "--no-load-images", action="store_true", dest="load_images", help="Do not load images")
opts.add_option("-p", "--parser", dest="parser", help="Choose a parser to use")

options, args = opts.parse_args()

kw_options = {}

if options.read_all:
    kw_options['read_all'] = True
elif options.max_read:
    kw_options['max_read_size'] = int(options.max_read_size)

if options.chunk_size:
    kw_options['chunk_size'] = int(options.chunk_size)

if options.use_js_ruleset:
    kw_options['use_js_ruleset'] = False

if options.parser:
    kw_options['parser'] = options.parser

if options.load_images:
    kw_options['load_images'] = False

kw_options['use_adblock_filters'] = options.use_adblock_filters
kw_options['debug'] = options.debug

try:
    url = args[0]
except IndexError:
    url = None
if options.url:
    url = options.url

if not url:
    print("URL required. Please use the url option or pass a url as the first argument")
    sys.exit(-1)

if options.benchmark:
    t1 = time.time()
else:
    t1 = 0

i = ImageResolver(**kw_options)
i.register(FileExtensionResolver(**kw_options))
i.register(WebpageResolver(**kw_options))

print(i.resolve(url))

if options.benchmark:
    print('TOTAL TIME', time.time() - t1)



