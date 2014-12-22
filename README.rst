=============
ImageResolver
=============

A python clone of ImageResolver for finding significant images in HTML content
See the excellent JS version at: https://github.com/mauricesvay/ImageResolver

USAGE
-----

::

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

* Loads as little of the image as possible when fetching for image info. Stops downloading if diminsions are found or a setable limit is reached.

* The original rules from the JS version are still implemented. (see options)

ImageResolver() METHODS
-----------------------

**__init__** *(\*\*kwargs)*

Keyword options

	* *max_read_size* - set to the maximum amount of bytes to read to find the width and height of an image. Default `10240`
	* *chunk_size* - set to the chunk size to read Default `1024`
	* *read_all* - set to read the entire image and then detect its info. Option will override max_read_size. Default `False`
	* *debug* - set to enable debugging output (logger="ImageResolver"). Default `False`

**fetch** *(string url)*

Fetches a URL and returns the response data.

**fetch_image_info** *(string url)*

Fetches an image url and examines the resulting image. Returns a tuple consisting of the detected file extension, the width and the height of the image.

**register** *(instance filter)*

Register a filter to examine an image with. The filter argument must be an instance of a class that has a `resolve()` method. `resolve()` must accept a string URL and must return a url or `None`

**resolve** *(string url)*

Loop through each registered filter until a url is resolved by one of them. If no url is found, returns `None`


FileExtensionResolver() METHODS
-------------------------------

**resolve** *(string url)*

Returns the url if the extention matches a possible image

ImgurPageResolver() METHODS
---------------------------

**resolve** *(string url)*

Returns an Imgur image url if `url` matches the pattern of an Imgur page

WebpageResolver() METHODS
-------------------------

The work-horse of this module. Our uses revolve mostly around this filter and thus it is the
most feature complete and tested.

**__init__** *(\*\*kwargs)*

Initialize the class with options:

	* *load_image* - set to true to load the first 1k of images whose size is not set in HTML. Default `False`
	* *use_js_ruleset* - set to true to use the original rules from the Javascript version. Default `False`
	* *use_adblock_filters* - set to false to disable adblock filters. Default `True`
	* *parser* - set to a BeautifulSoup compatable parser (lxml is recommended). Default `html.parser`
	* *blacklist* - set to a file containing AdBlockPlus style filters used to lower an image's score. Default `blacklist.txt`
	* *whiltelist* - set to a file containing AdBlockPlus style filters used to raise an image's score. Default `whitelist.txt`
	* *significant_surface* - Amount of surface (width x height) of the image required to add additional scoring
	* *boost_jpeg* - add (int) boost score to JPEG files. Default `1`
	* *boost_gif* - add (int) boost score to GIF files. Default `0`
	* *boost_png* - add (int) boost score to PNG files. Default `0`
	* *skip_fetch_errors* - Skip exceptions raised by fetch_image_info(). Exceptions are logged and the image will be skipped. Default `True`

The default parser for BeautifulSoup is html.parser which is built-in to python. We *highly* recommend you install lxml and pass parser="lxml"
to WebpageResolver(). In our testing we found that it was much faster and more accurate. 

LOGGING
-------

Use the name "ImageResolver" to configure a logger. Skipped exceptions will be logged to this logger's error output and when enabled, debugging output as well.

EXCEPTIONS
----------

**ImageInfoException**

Raised if the image could not be read or type, width or height properties return undefined. 
By default this exception is skipped and logged but can be enabled with "skip_fetch_errors=False" option in WebpageResolver

**HTTPException**

Raised if the image could not be loaded from the URL. 
By default this exception is skipped and logged but can be enabled with "skip_fetch_errors=False" option in WebpageResolver

TODO
-----------------

Still missing the following resolvers:

* ImgurAlbumResolver()

* FlickrResolver()

* OpengraphResolver()

* InstagramResolver()

I have no plans to implement a 9gag resolver.

Need to implement better caching. Future plan is to include a configurable cache method so images seen across sessions can be cached for better performance


AUTHOR
------

Chris Brown

BUGS
----

Probably. Send us an email or a patch if you find one

COPYRIGHT / ACKNOWLEDGEMENTS
----------------------------

Copyright (c) 2014 Constituent Voice, LLC.

Original idea and basic setup came from Maurice Svay https://github.com/mauricesvay/ImageResolver

Image detection came from the bfg-pages project https://code.google.com/p/bfg-pages/

Reading AdBlock Plus filters forked from https://github.com/wildgarden/abpy

LICENSE
-------

Some of the source libraries are licensed with the BSD license. To avoid license messiness we've chosen to release this software as BSD as well.
The easylist.txt provided by AdBlockPlus is licensed as GPL and it should be updated regularly anyway. For these reasons we have chosen not to
include the file in the package. You can pass it as the "blacklist" or "whitelist" parameter to the Webpageresolver


