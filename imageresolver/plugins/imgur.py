import re
import os
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import logging

class Plugin:
	def get_image(self, url, soup):
		if re.search('http(s*):\/\/(i\.|m\.)*imgur.com\/(gallery\/){0,1}(.*)', url):
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
			parsed = urlparse(url)

			if parsed.path[1:8] == 'gallery':
				logger.debug('Detected imgur gallery.')
				tag = soup.find('div', {'id':'1','class':'album-image'})
				image = re.findall('i\.imgur.com\/.*\.\w+', str(tag))
				if len(image) >= 1:
					return 'http://' + image[0]
			
			elif parsed.path[0:3] == '/a/':
				logger.debug('Detected imgur album.')
				tag = soup.find('meta',{'name':'twitter:image0:src'})
				if tag:
					return tag['content']

			else:
				parsed = urlparse(url)
				if re.search('imgur.com(:80)*', parsed.netloc) and os.path.basename(parsed.path):
					return 'http://i.imgur.com/' + os.path.basename(parsed.path) + '.jpg'
		return None

