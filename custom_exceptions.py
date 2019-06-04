class UrlInvalidError(Exception):
    def __str__(self):
        return 'Invalid url'


class ImageInvalidError(Exception):
    def __str__(self):
        return 'Invalid image'


class Base64ImageError(Exception):
    def __str__(self):
        return 'Image is encoded in base64, not yet supported'
