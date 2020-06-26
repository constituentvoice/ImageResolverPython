import re
import os
import logging
from operator import itemgetter
from imageresolver import FileExtensionResolver

class Plugin(object):
    def get_image(self, url, soup):

        ogtags = [{'type': 'facebook', 'attribute': 'property', 'name': 'og:image', 'value': 'content'},
                  {'type': 'facebook', 'attribute': 'rel', 'name': 'image_src', 'value': 'href'},
                  {'type': 'twitter', 'attribute': 'name', 'name': 'twitter:image', 'value': 'value'},
                  {'type': 'twitter', 'attribute': 'name', 'name': 'twitter:image', 'value': 'content'},
                  {'type': 'twitter', 'attribute': 'property', 'name': 'twitter:image', 'value': 'content'},
                  {'type': 'image', 'attribute': 'itemprop', 'name': 'image', 'value': 'content'}]

        ogimages = []

        for ogtag in ogtags:
            tags = soup.find_all('meta', {ogtag['attribute']: ogtag['name']})
            if tags:
                try:
                    for image in tags:
                        url = FileExtensionResolver().resolve(image['url'])
                        if url:
                            ogimages.append({'url': url, 'type': ogtag['type'], 'score': 0})
                except KeyError as e:
                    pass

        ogimages_len = len(ogimages)

        # if more than 1 image, score and return the best one
        if ogimages_len >= 1:
            if ogimages_len == 1:
                logger = logging.getLogger('ImageResolver')
                logger.debug('Resolving using plugin ' + str(os.path.basename(__file__)) + ' ' + str(url))
                resolved_image = ogimages[0]['url']
            else:
                for image in ogimages:
                    # sometimes opengraph tags don't have an actual image?
                    url = FileExtensionResolver().resolve(image['url'])
                    if not url:
                        image['score'] = -1
                    else:
                        if re.search('(large|big)', image['url'], re.IGNORECASE):
                            image['score'] += 1
                        if image['type'] == 'twitter':
                            image['score'] += 1

                ogimages.sort(key=itemgetter('score'), reverse=True)
                resolved_image = ogimages[0]['url']

            if not re.search('^https?:', resolved_image):
                if resolved_image.startswith('//'):
                    return 'https:' + resolved_image
            else:
                return resolved_image

        return None
