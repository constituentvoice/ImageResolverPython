__all__ = ['ImageResolverError', 'HTTPException', 'ImageInfoException']


class ImageResolverError(Exception):
    pass


# raised if a resource could not be loaded
class HTTPException(ImageResolverError):
    pass


# raised if getimageinfo returns null or otherwise unrecognizable
class ImageInfoException(ImageResolverError):
    pass

