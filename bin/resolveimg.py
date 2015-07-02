#!/usr/bin/env python

import sys
import imageresolver
import logging
import time
from optparse import OptionParser

logger = logging.getLogger('ImageResolver')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

opts = OptionParser()
opts.add_option("-u","--url",dest="url",help="A url to parse")
opts.add_option("-d","--debug", action="store_true", dest="debug", help="enable debugging")
opts.add_option("-r","--max-read", dest="max_read",help="Set the max read size")
opts.add_option("-c","--chunk-size",dest="chunk_size",help="Chunk size to read on each pass")
opts.add_option("-a","--read-all",dest="read_all",help="Read the entire image before checking size. Useful for some JPGs. Overrides --max-read")
opts.add_option("--no-adblock", action="store_true",dest="use_adblock_filters",help="Do not use whitelist.txt or blacklist.txt adblock filters")
opts.add_option("--no-ruleset", action="store_true",dest="use_js_ruleset",help="Do not use a custom ruleset for scoring.")
opts.add_option("--benchmark", action="store_true",dest="benchmark",help="Benchmark the total time it takes for the script to return an image")
opts.add_option("-l","--load-images", action="store_true",dest="load_images",help="Load images")
opts.add_option("-p","--parser", dest="parser",help="Choose a parser to use")

(options,args) = opts.parse_args()

kw_options = {}
if options.read_all:
	kw_options['read_all'] = True
elif options.max_read:
	kw_options['max_read_size'] = int(options.max_read_size)

if options.chunk_size:
	kw_options['chunk_size'] = int(options.chunk_size)

if options.use_adblock_filters:
	kw_options['use_adblock_filters'] = False

if options.use_js_ruleset:
	kw_options['use_js_ruleset'] = False

if options.parser:
	kw_options['parser'] = options.parser

kw_options['debug'] = options.debug
kw_options['load_images'] = options.load_images

try:
	url = args[0]
except IndexError:
	url = None
if options.url:
	url = options.url

if not url:
	print "URL required. Please use the url option or pass a url as the first argument"
	sys.exit(-1)

	
if options.benchmark:
	t1 = time.time()

i = imageresolver.ImageResolver(**kw_options)
i.register(imageresolver.FileExtensionResolver())
i.register(imageresolver.PluginResolver())
i.register(imageresolver.WebpageResolver(**kw_options))

print i.resolve(url)

if options.benchmark:
	print 'TOTAL TIME', time.time() - t1

