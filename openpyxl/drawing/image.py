from __future__ import absolute_import
from __future__ import division
# Copyright (c) 2010-2019 openpyxl

from io import BytesIO

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = False

from openpyxl.compat import basestring

def bounding_box(bw, bh, w, h):
    """
    Returns a tuple (new_width, new_height) which has the property
    that it fits within box_width and box_height and has (close to)
    the same aspect ratio as the original size
    """
    new_width, new_height = w, h
    if bw and new_width > bw:
        new_width = bw
        new_height = new_width / (w / h)
    if bh and new_height > bh:
        new_height = bh
        new_width = new_height * (w / h)
    return (new_width, new_height)


def _import_image(img):
    if not PILImage:
        raise ImportError('You must install Pillow to fetch image objects')

    if not isinstance(img, PILImage.Image):
        img = PILImage.open(img)

    return img


class Image(object):
    """Image in a spreadsheet"""

    _id = 1
    _path = "/xl/media/image{0}.{1}"
    anchor = "A1"

    def __init__(self, img):

        self.ref = img
        mark_to_close = isinstance(img, basestring)
        image = _import_image(img)
        self.width, self.height = image.size
        try:
            self.format = image.format.lower()
        except AttributeError:
            self.format = "png"
        if mark_to_close:
            # PIL instances created for metadata should be closed.
            image.close()


    def _data(self):
        """
        Return image data, convert to supported types if necessary
        """
        img = _import_image(self.ref)
        # don't convert these file formats
        if self.format in ['gif', 'jpeg', 'png']:
            img.fp.seek(0)
            fp = img.fp
        else:
            fp = BytesIO()
            img.save(fp, format=self.format)

        return fp.read()


    @property
    def path(self):
        return self._path.format(self._id, self.format)
