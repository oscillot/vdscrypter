from PIL import Image

from vdscrypter.exceptions import InitializationError


class Video(object):
    """An uninitialized video object"""
    def __init__(self):
        self.initialized = False

    def new(self, width, height, color="black"):
        """Initializes the video object as a new video"""
        if self.initialized:
            raise InitializationError('Already initialized.')
        image = Image.new("RGB", (width, height), color)
