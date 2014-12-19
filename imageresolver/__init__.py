"""
ImageResolver.py
Copyright 2013 National Write Your Congressman

ImageResolver.py is a port of the excellent ImageResolver
javascript library by Maurice Svay
https://github.com/mauricesvay/ImageResolver
"""

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


class HTTPException(Exception):
	pass

class ImageResolver():
	
	def __init__(self,**kwargs):
		self.filters = [];
		self.cache = {}
		self.debug = kwargs.get('debug',False)

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
			imgheader = None
			for chunk in r.iter_content(1024):
				imgheader = chunk
				r.close()
				break
			
			(content, width, height) = getimageinfo.getImageInfo(imgheader)
			logger.debug( 'Detected ' + str(content) + ' ' + str(width) + 'x' + str(height) )

			ext = None
			if content == 'image/png':
				ext = '.png'
			elif content == 'image/gif':
				ext = '.gif'
			elif content == 'image/jpeg':
				ext = '.jpg'

			return ext,width,height
		else:
			logger.debug('Fetch failed with status code ' + str(r.status_code))

		return None,None,None


	
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

class FileExtensionResolver():
	def resolve(self,url,**kwargs):
		logger.debug('Resolving using file extension ' + str(url))
		parsed = urlparse(url)
		path = parsed.path
		
		if re.search('(png|jpg|jpeg|gif|bmp|svg)$',path, re.I):
			return url

		return None

class ImgurPageResolver():
	# works a little different than the JS version. 
	# it should drop references to galleries and find the image
	# could be buggy!
	def resolve(self,url,**kwargs):
		logger.debug('Resolving using Imgur ' + str(url))
		parsed = urlparse(url)
		if re.search( 'imgur.com(:80)*', parsed.netloc) and os.path.basename(parsed.path):
			return 'http://i.imgur.com/' + os.path.basename(parsed.path) + '.jpg'

		return None

class WebpageResolver():
	def __init__(self,**kwargs):
		self.load_images = kwargs.get('load_images',False)
		self.use_js_ruleset = kwargs.get('use_js_ruleset',False)
		self.use_adblock_filters = kwargs.get('use_adblock_filters',True)
		
		cwd = os.path.dirname(__file__)
		if not cwd:
			cwd = '.'

		self.parser = kwargs.get('parser','html.parser') # default html.parser is built-in but lots of failure. lxml is recommended
		self.blacklist = kwargs.get('blacklist', os.path.join(cwd,'data', 'blacklist.txt'))
		self.whitelist = kwargs.get('whitelist', os.path.join(cwd,'data', 'whitelist.txt'))
		if self.use_adblock_filters:
			self.abpy_black = abpy.Filter(open(self.blacklist))
			self.abpy_white = abpy.Filter(open(self.whitelist))

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
			black_matches = self.abpy_black.match(src)
			try:
				score = len(black_matches) * -1
			except:
				score = 0


			white_matches = self.abpy_white.match(src)

			try:
				score += len(white_matches)
			except:
				if not score:
					score = 0

			logger.debug('score set to ' + str(score) + ' using ABP filters')

		return score

	def resolve(self,url,**kwargs):
		logger.debug('Resolving as a webpage ' + str(url))

		ir = ImageResolver()
		content = ir.fetch(url)
		soup = BeautifulSoup(content,self.parser)
		images = soup.find_all('img')

		candidates = []
		significant_surface = 16*16
		significant_surface_count = 0
		src = None

		logger.debug('Found ' + str( len(images) ) + ' candidate images')

		for i in images:
			surface = 0
			src = i.get('src',i.get('data-src', i.get('data-lazy-src')))
			if not src:
				logger.debug('No source found. Skipping')
				continue
			else:
				logger.debug('Checking ' + str(src))

				# get the absolute path to the image
				if not re.search('^https?:\/\/',src):
					parts = urlparse(url)
					
					if src[0] == '/':
						src = parts.scheme + '://' + parts.netloc + src
					else:
						path = os.path.dirname(parts.path)
						src = parts.scheme + '://' + parts.netloc + path + '/' + src

				logger.debug('Parsed full url as ' + str(src))
				i['src'] = src # forces setting it to whatever we found so we don't parse it in _score()

			# get the score first since getting the surface is potentially more intensive now
			score = self._score(i)
			
			if score >= 0:
				logger.debug('Image has a score, checking size')
				# differece: The JS library's default surface is 0. Ours is 1
				# it shouldn't matter

				width = i.get('width',"1")
				height = i.get('height',"1")

				if re.search('\D+',width):
					width = re.sub('\D+','',width)

				if re.search('\D+',height):
					height = re.sub('\D+','',height)

				try:
					width = int(width)
					height = int(height)
					logger.debug('detected dimensions ' + str(width) + 'x' + str(height))

				except ValueError:
					width = 1
					height = 1
					logger.debug( 'no html diminsions detected' )

				surface = width * height

				logger.debug('set surface to ' + str(surface) )

				# try to obtain the size from the headers of the image
				if surface < 2 and self.load_images:
					logger.debug('surface was too small. Attempting to load image')
					(ext,width,height) = ir.fetch_image_info(src)
					if ext:
						surface = width * height
						logger.debug('new surface is ' + str(surface) )
					else:
						logger.debug('No usable info from image')

				if surface > significant_surface:
					significant_surface_count += 1

				#score = self._score(i) # Why was this here???
				
				candidates.append({
					'url': src,
					'surface': surface,
					'score': score
				})

		if len(candidates) <= 0:
			return None

		# sort by surface and score if we can
		if significant_surface_count > 0:
			candidates = sorted( candidates, key=operator.itemgetter('surface','score'), reverse=True)
		else:
			candidates = sorted( candidates,key=operator.itemgetter('score'),reverse=True)
		
		if kwargs.get('debug'):
			for c in candidates:
				logger.debug(c.get('url') + ' surface: ' + str(c.get('surface')) + ' score: ' + str(c.get('score')))

		image = candidates[0].get('url')

		return image
