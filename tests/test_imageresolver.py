from __future__ import absolute_import
import unittest
from imageresolver import ImageResolver, FileExtensionResolver, WebpageResolver


class TestImageResolver(unittest.TestCase):
	def setUp(self):
		# set to an imgur page
		self.imgur_page = 'https://imgur.com/adtBv9Y'

		# set to the expected result of the imgur page
		# also checks the file extension
		self.imgur_result = 'https://i.imgur.com/adtBv9Y.jpg'

		# set to a web url
		self.web_url = 'https://xkcd.com/353/'

		# set to the expected return image from the web url
		self.web_img = 'https://imgs.xkcd.com/comics/python.png'

	def test_fetch_image_info(self):
		i = ImageResolver()
		(ext, width, height) = i.fetch_image_info(self.web_img)

		self.assertEquals(ext, '.png')
		self.assertEquals(width, 518)
		self.assertEquals(height, 588)

	def test_resolve_fileext(self):
		i = ImageResolver()
		i.register(FileExtensionResolver())
		src = i.resolve(self.web_img)

		self.assertEquals(src, self.web_img)

	def test_resolve_webpage(self):
		i = ImageResolver()
		i.register(WebpageResolver(load_images=True))
		src = i.resolve(self.web_url)
		self.assertEquals(src, self.web_img)

