import sys
from os.path import dirname,abspath
sys.path.append( dirname( dirname( abspath(__file__)) ) )
import imageresolver

i = imageresolver.ImageResolver()
i.register(imageresolver.FileExtensionResolver())
i.register(imageresolver.ImgurPageResolver())
i.register(imageresolver.WebpageResolver(load_images=True, parser='lxml'))
f = sys.argv[1]

print i.resolve(f)
