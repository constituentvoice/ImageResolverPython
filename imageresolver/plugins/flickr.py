import re
import os
import logging


class Plugin(object):
	@staticmethod
	def get_image(url, soup):
		if re.search('http(s*):\/\/www.flickr.com\/photos\/([^\/]*)\/([^\/]*)\/(.*)', url):
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin {} {}'.format(os.path.basename(__file__), url))
			tag = soup.find('img', {'class': 'main-photo'})
			if tag:
				return 'https: {}'.format(tag['src'])
		return None
