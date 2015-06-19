import sys
import unittest
import requests
from os.path import dirname,abspath
sys.path.append( dirname( dirname( dirname( abspath(__file__)) ) ) )
from imageresolver import ImageResolver, FileExtensionResolver, ImgurPageResolver, WebpageResolver

class TestImageResolver(unittest.TestCase):
	def setUp(self):
		# set to an imgur page
		self.imgur_page = 'http://imgur.com/adtBv9Y'

		# set to the expected result of the imgur page
		# also checks the file extension
		self.imgur_result = 'http://i.imgur.com/adtBv9Y.jpg'

		# set to a web url
		self.web_url = 'http://xkcd.com/353/'

		# set to the expected return image from the web url
		self.web_img = 'http://imgs.xkcd.com/comics/python.png'

	def test_fetch_image_info(self):
		i = ImageResolver()
		(ext,width,height) = i.fetch_image_info(self.web_img)

		self.assertEquals(ext,'.png')
		self.assertEquals(width,518)
		self.assertEquals(height,588)
	
	def test_resolve_imgur(self):
		i = ImageResolver()
		i.register(ImgurPageResolver())
		src = i.resolve(self.imgur_page)
		self.assertEquals(src,self.imgur_result)

	def test_resolve_fileext(self):
		i = ImageResolver()
		i.register(FileExtensionResolver())
		src = i.resolve(self.web_img)

		self.assertEquals(src,self.web_img)

	def test_resolve_webpage(self):
		i = ImageResolver()
		i.register(WebpageResolver(load_images=True))
		src = i.resolve(self.web_url)
		self.assertEquals(src, self.web_img )

