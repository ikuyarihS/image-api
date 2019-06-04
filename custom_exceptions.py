class UrlInvalidError(Exception):
    def __str__(self):
        return 'Invalid url'


class ImageInvalidError(Exception):
    def __str__(self):
        return 'Invalid image'
