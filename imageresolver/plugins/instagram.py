import re
import os
import logging
from bs4 import BeautifulSoup

class Plugin:
	def get_image(self, url, soup):
		if re.search('http(s*):\/\/instagr(\.am|am\.com)\/p\/([^\/]+)', url):
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
			tag = soup.find('meta',{'property':'og:image'})
			if tag:
				return tag['content']
		return None
