"""
ImageResolver
Copyright 2020 Constituent Voice LLC
http://constituentvoice.com/
http://github.com/constituentvoice

ImageResolver is a port of the excellent ImageResolver
javascript library by Maurice Svay
https://github.com/mauricesvay/ImageResolver
"""

from imageresolver.base import FileExtensionResolver, ImageResolver, WebpageResolver
from imageresolver.getimageinfo import getImageInfo
from imageresolver.version import __version__

__all__ = ['ImageResolver', 'FileExtensionResolver', 'WebpageResolver', '__version__']
