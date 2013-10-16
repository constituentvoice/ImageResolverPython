=============
ImageResolver
=============

A python clone of ImageResolver for finding significant images in HTML content
See the excellent JS version at: https://github.com/mauricesvay/ImageResolver

Differences From the Javascript Version
---------------------------------------

* methods return instead of calling callbacks

* WebpageResolver has lots of new options (see below)

* Added some debugging features

* Exceptions are raised rather than callback to an error function

WebpageResolver Additions
-------------------------

* rules syntax is now based on AdBlockPlus filters (https://adblockplus.org/en/filters)

* New rules can be added without writing a resolver

* blacklist image sources and whitelist

* Can load the first 1k of images found in the page to determine dimensions if the attributes are not includes

* The original rules from the JS version are still implemented. (see options)

Webpage Resolver options
------------------------

Options to pass to the webpage resolver. Default values are shown.
	
	# set to true to load the first 1k of images whose size is not set in HTML
	load_images=False

	# set to true to use the original rules from the Javascript version
	use_js_ruleset=False

	# set to false to disable adblock filters
	use_adblock_filters=True

	# set to a BeautifulSoup compatable parser (lxml is recommended)
	parser='html.parser'

	# set to a file containing AdBlockPlus style filters that will lower an
	# image's score
	blacklist='blacklist.txt'

	# set to a file containing AdBlockPlus style filters that will raise an
	# image's score
	whitelist='whitelist.txt'

The default parser for BeautifulSoup is html.parser which is built-in to python. We *highly* recommend you install lxml and pass parser="lxml"
to WebpageResolver(). In our testing we found that it was much faster and more accurate. 

Currently Implemented Resolvers
-------------------------------

* FileExtensionResolver()

* ImgurPageResolver()

* WebpageResolver()

To Be Implemented
-----------------

* ImgurAlbumResolver()

* FlickrResolver()

* OpengraphResolver()

* InstagramResolver()

I have no plans to implement a 9gag resolver.

USAGE
-----

	import imageresolver
	import sys

	try:
		i = imageresolver.ImageResolver()
		i.register(imageresolver.FileExtensionResolver())
		i.register(imageresolver.ImgurPageResolver())
		i.register(imageresolver.WebpageResolver(load_images=True, parser='lxml',blacklist='easylist.txt'))
		url = sys.argv[1]

		print i.resolve(url)
	except:
		print "An error occured"


AUTHOR
------

Chris Brown

BUGS
----

Probably. Send us an email or a patch if you find one

COPYRIGHT / ACKNOWLEDGEMENTS
----------------------------

(c) 2013 National Write Your Congressman

Original idea and basic setup came from Maurice Svay https://github.com/mauricesvay/ImageResolver

Image detection came from the bfg-pages project https://code.google.com/p/bfg-pages/

Reading AdBlock Plus filters forked from https://github.com/wildgarden/abpy

LICENSE
-------

Some of the source libraries are licensed with the BSD license. To avoid license messiness we've chosen to release this software as BSD as well.
The easylist.txt provided by AdBlockPlus is licensed as GPL and it should be updated regularly anyway. For these reasons we have chosen not to
include the file in the package. You can pass it as the "blacklist" or "whitelist" parameter to the Webpageresolver


