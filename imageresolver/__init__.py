"""
ImageResolver
Copyright 2014 Constituent Voice LLC
http://constituentvoice.com/
http://github.com/constituentvoice

ImageResolver is a port of the excellent ImageResolver
javascript library by Maurice Svay
https://github.com/mauricesvay/ImageResolver
"""

from __future__ import division 
import requests
import re
from urlparse import urlparse
import os.path
import operator
from bs4 import BeautifulSoup
import sys
import logging

logger = logging.getLogger('ImageResolver')

# add the vendor directories to our path
module_path = os.path.dirname(__file__)
if not module_path:
	module_path = '.'

sys.path.append(module_path)

from .abpy import abpy
from . import getimageinfo
from .version import __version__

# raised if a resource could not be loaded
class HTTPException(Exception):
	pass

# raised if getimageinfo returns null or otherwise unrecognizable
class ImageInfoException(Exception):
	pass

class ImageResolver(object):
	
	def __init__(self,**kwargs):
		self.filters = [];
		self.cache = {}
		self.debug = kwargs.get('debug',False)
		# how much should I try to read of an image before giving up and returning nothing
		self.max_read = kwargs.get('max_read_size',10240)

		# size of chunk to read
		self.chunk_size = kwargs.get('chunk_size',1024)

		# read the entire image before trying to get its information
		self.read_all = kwargs.get('read_all',False)

		if self.debug:
			logger.setLevel(logging.DEBUG)

	def fetch(self,url):
		cache = self.cache
		if cache.get(url):
			logger.debug('Loading ' + str(url) + ' from cache')
			return cache.get(url)
		else:
			logger.debug('Loading ' + str(url))
			resp = requests.get(url)
			if resp.status_code == 200:
				cache[url] = resp.text
				return cache.get(url)
			else:
				raise HTTPException(resp)

	def fetch_image_info(self,url):
		logger.debug('Fetching raw image info ' + str(url) )
		r = requests.get(url,stream=True)
		if r.status_code == 200:
			imgheader = b''
			found = False
			read = 0

			for chunk in r.iter_content(self.chunk_size):
				read += self.chunk_size
				imgheader += chunk
				if not self.read_all:
					(content, width, height) = getimageinfo.getImageInfo(imgheader)
					if content and width and height:
						found = True
						break

					# break if we've read enough
					if self.max_read > -1 and read >= self.max_read:
						break

			r.close() # close the connection

			if self.read_all:
				(content, width, height) = getimageinfo.getImageInfo(imgheader)
				found = True
				r.close()


			logger.debug( 'Detected ' + str(content) + ' ' + str(width) + 'x' + str(height) )

			ext = None
			if content == 'image/png':
				ext = '.png'
			elif content == 'image/gif':
				ext = '.gif'
			elif content == 'image/jpeg':
				ext = '.jpg'
			
			if not found or not ext:
				raise ImageInfoException('getimageinfo() could not detect the image attributes properly')

			return ext,width,height
		else:
			logger.debug('Fetch failed with status code ' + str(r.status_code))
			raise HTTPException('Fetch image %s failed with status code %d' % (url,r.status_code))

	
	def register(self,f):
		self.filters.append(f)

	# I don't think we need this
	def next(self,filters,url,callback):
		pass
	
	# instead of using next() we just loop through the filters
	# until we find one that returns
	def resolve(self,url):
		logger.debug('Attempting to resolve ' + str(url))
		for f in self.filters:
			resp = f.resolve(url,debug=self.debug)
			
			# returns the first filter that gives us something
			if resp:
				return resp

class FileExtensionResolver(object):
	def resolve(self,url,**kwargs):
		logger.debug('Resolving using file extension ' + str(url))
		parsed = urlparse(url)
		path = parsed.path
		
		if re.search('(png|jpg|jpeg|gif|bmp|svg)$',path, re.I):
			return url

		return None

class ImgurPageResolver(object):
	# works a little different than the JS version. 
	# it should drop references to galleries and find the image
	# could be buggy!
	def resolve(self,url,**kwargs):
		logger.debug('Resolving using Imgur ' + str(url))
		parsed = urlparse(url)
		if re.search( 'imgur.com(:80)*', parsed.netloc) and os.path.basename(parsed.path):
			return 'http://i.imgur.com/' + os.path.basename(parsed.path) + '.jpg'

		return None

class WebpageResolver(object):
	def __init__(self,**kwargs):
		self.load_images = kwargs.get('load_images',False)
		self.use_js_ruleset = kwargs.get('use_js_ruleset',False)
		self.use_adblock_filters = kwargs.get('use_adblock_filters',True)
		self.significant_surface = kwargs.get('significant_surface', 100*100)
		
		cwd = os.path.dirname(__file__)
		if not cwd:
			cwd = '.'

		self.parser = kwargs.get('parser','html.parser') # default html.parser is built-in but lots of failure. lxml is recommended
		self.blacklist = kwargs.get('blacklist', os.path.join(cwd,'data', 'blacklist.txt'))
		self.whitelist = kwargs.get('whitelist', os.path.join(cwd,'data', 'whitelist.txt'))

		self.boost_jpeg = kwargs.get('boost_jpeg', 1)
		self.boost_gif = kwargs.get('boost_gif', 0)
		self.boost_png = kwargs.get('boost_png', 0)
		self.skip_fetch_errors = kwargs.get('skip_fetch_errors',True)

		self.abpy_black = None
		self.abpy_white = None

		if self.use_adblock_filters:
			try:
				self.abpy_black = abpy.Filter(open(self.blacklist))
			except:
				logger.warning('Unable to load black list file, %s.' % self.blacklist )

			try:
				self.abpy_white = abpy.Filter(open(self.whitelist))
			except:
				logger.warning('Unable to load white list file, %s.' % self.whitelist )

	def _score(self,image):
		score = 0
		src = image.get('src')
		
		if not src:
			return 0

		if self.use_js_ruleset:
			# use the original rules from the js library
			
			rules = [
				{'pattern':'(large|big)','score':1},
				{'pattern':'upload','score':1},
				{'pattern':'media','score':1},
				{'pattern':'gravatar.com','score':-1},
				{'pattern':'feeds.feedburner.com','score':-1},
				{'pattern':'icon','score':-1},
				{'pattern':'logo','score':-1},
				{'pattern':'spinner','score':-1},
				{'pattern':'loading','score':-1},
				{'pattern':'1x1','score':-1},
				{'pattern':'pixel','score':-1},
				{'pattern':'ads','score':-1},
			]
			
			for r in rules:
				if re.search( r.get('pattern'), src, re.I ):
					score += r.get('score')

			logger.debug('score set to ' + str(score) + ' using JS filters')

		if self.use_adblock_filters:
			# just detect ads using AdBlockPlus filters (default)
			no_filters = True
			if self.abpy_black:
				no_filters = False
				black_matches = self.abpy_black.match(src)
				try:
					score = len(black_matches) * -1
				except:
					score = 0

			if self.abpy_white:
				no_filters = False
				white_matches = self.abpy_white.match(src)

				try:
					score += len(white_matches)
				except:
					if not score:
						score = 0

			logger.debug('score set to ' + str(score) + ' using ABP filters')

		if not self.use_js_ruleset and ( not self.use_adblock_filters or no_filters ):
			logger.warning('No filters were enabled!')

		return score

	def resolve(self,url,**kwargs):
		logger.debug('Resolving as a webpage ' + str(url))

		ir = ImageResolver()
		content = ir.fetch(url)
		soup = BeautifulSoup(content,self.parser)
		images = soup.find_all('img')

		candidates = []
		significant_surface = self.significant_surface
		current_image = None
		current_image_score = None
		src = None
		src_cache = {}

		logger.debug('Found ' + str( len(images) ) + ' candidate images')
	
		# get url parts for building image srcs
		parts = urlparse(url)

		for i in images:
			surface = 0
			score = 0
			src = i.get('src',i.get('data-src', i.get('data-lazy-src')))
			if not src:
				logger.debug('No source found. Skipping')
				continue
			else:
				logger.debug('Checking ' + str(src))

				# get the absolute path to the image
				if not re.search('^https?:\/\/',src):
					# url parse doesn't recognize data: as valid
					if re.search('^data:', src):
						# skip data urls
						continue
					else:
					
						if src[0] == '/':
							# check protocol-less urls
							if src[1] == '/':
								src = parts.scheme + ':' + src
							else:
								src = parts.scheme + '://' + parts.netloc + src
						else:
							path = os.path.dirname(parts.path)
							src = parts.scheme + '://' + parts.netloc + path + '/' + src

				logger.debug('Parsed full url as ' + str(src))
				i['src'] = src # forces setting it to whatever we found so we don't parse it in _score()
			
			if src_cache.get(src):
				# skip already parsed image
				# reduce its score if its the current image. Appearing more than
				# once tends to be an indicator that we don't care about it
				if src == current_image:
					current_image_score -= 1
				continue
			else:
				src_cache[src] = True

			# get the score first since getting the surface is potentially more intensive now
			score += self._score(i)
			
			if score >= 0:
				logger.debug('Image has a score, ' + str(score) + ' checking size')
				# differece: The JS library's default surface is 0. Ours is 1
				# it shouldn't matter

				# Edit: it matters because there's no reason to download 1x1 gifs

				width = i.get('width',"0")
				height = i.get('height',"0")

				if re.search('\D+',width):
					width = re.sub('\D+','',width)

				if re.search('\D+',height):
					height = re.sub('\D+','',height)

				try:
					width = int(width)
					height = int(height)

					# if we found diminsions and one of them was 0 or null then
					# go ahead and set it to 1 to ensure there is a surface
					if width == 0 and height > 0:
						width = 1
					elif height == 0 and width > 0:
						height = 1

					logger.debug('detected dimensions ' + str(width) + 'x' + str(height))
					surface = width * height
					logger.debug('set surface to ' + str(surface) )

				except ValueError:
					width = 0
					height = 0
					logger.debug( 'no html diminsions detected' )


				# try to obtain the size from the headers of the image
				if surface < 1 and self.load_images:
					logger.debug('surface was too small. Attempting to load image')
					try:
						(ext,width,height) = ir.fetch_image_info(src)
					except (HTTPException, ImageInfoException) as e:
						if self.skip_fetch_errors:
							logger.error( repr(e) )
							# ignore this one and move on
							continue
						else:
							raise

					if ext:
						surface = width * height
						logger.debug('new surface is ' + str(surface) )
						
						if self.boost_jpeg and ext == '.jpg':
							score += self.boost_jpeg
						elif self.boost_gif and ext == '.gif':
							score += self.boost_gif
						elif self.boost_png and ext == '.png':
							score += self.boost_png
					else:
						logger.debug('No usable info from image')

				if surface > significant_surface:
					modifier = surface // significant_surface
					score += modifier
				
				logger.debug('%s surface: %d, score: %d' % (url,surface,score) )

				if current_image_score == None or current_image_score < score:
					current_image = src
					current_image_score = score

					logger.debug('Set current image %s' % url )

		return current_image
