import re
import os
import requests
import logging
from bs4 import BeautifulSoup

class Plugin:
	def get_image(self, url, soup):
		if re.search('http(s*):\/\/www.flickr.com\/photos\/([^\/]*)\/([^\/]*)\/(.*)', url):
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
			tag = soup.find('img', {'class':'main-photo'})
			if tag:
				return 'https:' + tag['src']
		return None
