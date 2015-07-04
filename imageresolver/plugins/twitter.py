import re
import os
import logging
from urlparse import urlparse
from bs4 import BeautifulSoup

class Plugin:
	def get_image(self, url, soup):
		if re.search('http(s*):\/\/(mobile\.|m\.)*twitter.com\/[a-zA-z0-9]*\/status\/\d+', url):
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
			parsed = urlparse(url)
			if parsed.netloc.split('.')[0] == 'mobile':
				tag = soup.find('img',{'class':'CroppedPhoto-img u-block'})
				if tag:
					return tag['src']
			
			else:
				tag = soup.find('meta',{'property':'og:image'})
				if tag:
					return tag['content']
