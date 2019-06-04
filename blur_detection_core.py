# import the necessary packages
from urllib.request import urlopen

import cv2
import numpy as np
import re

from custom_exceptions import ImageInvalidError, UrlInvalidError

IMAGE_EXTENSIONS = [
    "jpeg",  # Joint Photographic Experts Group
    "jpg",  # Joint Photographic Experts Group
    "png",  # Portable Network Graphics
    "gif",  # Graphics Interchange Format
    "tiff",  # Tagged Image File
    "psd",  # Photoshop Document
    "pdf",  # Portable Document Format
    "eps",  # Encapsulated Postscript
    "ai",  # Adobe Illustrator Document
    "indd",  # Adobe Indesign Document
    "raw",  # Raw Image Formats
]

REGEX_IMAGE_CHECK = re.compile('|'.join(IMAGE_EXTENSIONS), re.IGNORECASE)


def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


def blur_check_link(url):
    if not REGEX_IMAGE_CHECK.findall(url):
        raise ImageInvalidError

    try:
        resp = urlopen(url)
    except ValueError:
        raise UrlInvalidError

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        raise ImageInvalidError

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    score = variance_of_laplacian(gray)
    return score
