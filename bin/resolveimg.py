#!/usr/bin/env python

import sys
import imageresolver
import logging
from optparse import OptionParser

logger = logging.getLogger('ImageResolver')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

opts = OptionParser()
opts.add_option("-u","--url",dest="url",help="A url to parse")
opts.add_option("-d","--debug", action="store_true", dest="debug", help="enable debugging")
opts.add_option("-r","--max-read", dest="max_read",help="Set the max read size")
opts.add_option("-c","--chunk-size",dest="chunk_size",help="Chunk size to read on each pass")
opts.add_option("-a","--read-all",dest="read_all",help="Read the entire image before checking size. Useful for some JPGs. Overrides --max-read")

(options,args) = opts.parse_args()

kw_options = {}
if options.read_all:
	kw_options['read_all'] = True
elif options.max_read:
	kw_options['max_read_size'] = int(options.max_read_size)

if options.chunk_size:
	kw_options['chunk_size'] = int(options.chunk_size)

kw_options['debug'] = options.debug

try:
	url = args[0]
except IndexError:
	url = None
if options.url:
	url = options.url

if not url:
	print "URL required. Please use the url option or pass a url as the first argument"
	sys.exit(-1)

i = imageresolver.ImageResolver(**kw_options)
i.register(imageresolver.FileExtensionResolver())
i.register(imageresolver.ImgurPageResolver())
i.register(imageresolver.WebpageResolver(load_images=True, parser='lxml'))

print i.resolve(url)

