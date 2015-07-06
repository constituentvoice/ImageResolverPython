import re
import os
import logging
from bs4 import BeautifulSoup
from operator import itemgetter

class Plugin:
	def get_image(self, url, soup):

		ogtags = [{'type':'facebook','attribute':'property', 'name':'og:image', 'value':'content'},
			{'type':'facebook','attribute':'rel', 'name':'image_src', 'value':'href'},
			{'type':'twitter','attribute':'name', 'name':'twitter:image', 'value':'value'},
			{'type':'twitter','attribute':'name', 'name':'twitter:image', 'value':'content'},
			{'type':'twitter','attribute':'property', 'name':'twitter:image', 'value':'content'},
			{'type':'image','attribute':'itemprop', 'name':'image', 'value':'content'}]

		ogimages = []		

		for ogtag in ogtags:
			tags = soup.find_all('meta', {ogtag['attribute']:ogtag['name']})
			if tags != []:
				for image in tags:
					try:
						ogimages = ogimages + [{'url':image[ogtag['value']], 'type':ogtag['type'], 'score':0} for image in tags]
					except KeyError as e:
						pass
		
		ogimages_len = len(ogimages)

		# if more than 1 image, score and return the best one
		if ogimages_len >= 1:
			if ogimages_len == 1:
				logger = logging.getLogger('ImageResolver')
				logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' +  str(url))
				resolved_image = ogimages[0]['url']
			else:
				for image in ogimages:
					if re.search('(large|big)', image['url'], re.IGNORECASE):
						image['score'] += 1
					if image['type'] == 'twitter':
						image['score'] += 1

				ogimages.sort(key=itemgetter('score'), reverse=True)
				resolved_image = ogimages[0]['url']
			
			if not re.search('^https?:', resolved_image):
				if resolved_image.startswith('//'):
					return 'http:' + resolved_image
			else:
				return resolved_image	
					

		return None

