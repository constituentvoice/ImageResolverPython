#!/usr/bin/env python

import sys
import imageresolver
import logging
from optparse import OptionParser

opts = OptionParser()
opts.add_option("-u","--url",dest="url",help="A url to parse")
opts.add_option("-d","--debug", action="store_true", dest="debug", help="enable debugging")
(options,args) = opts.parse_args()

print args
"""
url = args[0]
if options.url

i = imageresolver.ImageResolver()
i.register(imageresolver.FileExtensionResolver())
i.register(imageresolver.ImgurPageResolver())
i.register(imageresolver.WebpageResolver(load_images=True, parser='lxml'))
f = sys.argv[1]

print i.resolve(f)
"""
