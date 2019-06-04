# import the necessary packages
import base64
import re

import cv2
import numpy as np
import requests

from custom_exceptions import (Base64ImageError, ImageInvalidError,
                               UrlInvalidError)

# List of all current known image extentions.
# I seriously doubt that we will use all of them.
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

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'

REGEX_IMAGE_CHECK = re.compile('|'.join(IMAGE_EXTENSIONS), re.IGNORECASE)
REGEX_BASE64 = re.compile('^data:image/.+;base64,', re.IGNORECASE)


def variance_of_laplacian(image):
    """Compute the Laplacian of the image and then return the focus
    measure, which is simply the variance of the Laplacian

    Arguments:
        image {numpy.array} -- Current image.
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()


def blur_check_file(file) -> float:
    """Get blur score of current images.
    Also raises UrlInvalidError and ImageInvalidError.

    Arguments:
        file {str} -- Image url passed into request.

    Returns:
        float -- Blur score.

    """
    npimg = np.fromstring(file.body, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    score = variance_of_laplacian(gray)
    return score


def blur_check_link(url: str) -> float:
    """Get blur score of current images.
    Also raises UrlInvalidError and ImageInvalidError.

    Arguments:
        url {str} -- Image url passed into request.

    Returns:
        float -- Blur score.

    """
    if not REGEX_IMAGE_CHECK.findall(url):
        raise ImageInvalidError

    if REGEX_BASE64.findall(url):
        raise Base64ImageError

    try:
        bytestream = requests.get(url, verify=True).content
    except ValueError:
        image_data = REGEX_BASE64.sub('', url)
        bytestream = base64.b64decode(image_data)
        with open("D:/Project/ImageProcessing/wtf/wat.jpg", "wb") as f:
            f.write(bytestream)
    except ValueError:
        raise UrlInvalidError

    image = np.asarray(bytearray(bytestream), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        raise ImageInvalidError

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    score = variance_of_laplacian(gray)
    return score
