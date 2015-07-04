import re
import os
import logging
from bs4 import BeautifulSoup

class Plugin:
	def get_image(self, url, soup):

		ogtags = [{'attribute':'property', 'name':'og:image', 'value':'content'},
			{'attribute':'rel', 'name':'image_src', 'value':'href'},
			{'attribute':'name', 'name':'twitter:image', 'value':'value'},
			{'attribute':'name', 'name':'twitter:image', 'value':'content'}]

		ogimages = []		

		for ogtag in ogtags:
			tags = soup.find_all('meta', {ogtag['attribute']:ogtag['name']})
			if tags != []:
				try:
					ogimages = ogimages + [image[ogtag['value']] for image in tags]
				except KeyError:
					pass
		
		if len(ogimages) >= 1:
			logger = logging.getLogger('ImageResolver')
			logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
			return ogimages[0]

		return None

