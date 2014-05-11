# import os
# import time
# import shutil
# import tempfile
# from PIL import Image
#
# from vdscrypter.exceptions import InitializationError
#
#
# class Video(object):
#     """An uninitialized video object"""
#     def __init__(self):
#         self.initialized = False
#         self.workspace = tempfile.mkdtemp()
#         self.original_file = None
#         self.fixed_file = None
#         self.is_animated = False
#         self.temp_file = os.path.join(self.workspace, str(int(time.time())))
#
#     def prevent_multiple_initializations(self):
#         if self.initialized:
#             raise InitializationError('Already initialized.')
#
#     def check_exists(self, asset):
#         if os.path.exists(asset):
#             self.original_file = asset
#             self.initialized = True
#         else:
#             raise ValueError('Not a valid file path!')
#
#     def is_image(self):
#         for fmat in ['.bmp', '.jpg', '.jpeg', 'gif', '.tga']:
#             #TODO consider using magic bytes to ID files better
#             if self.original_file.endswith(fmat):
#                 return True
#         return False
#
#     def is_jpeg(self):
#         for fmat in ['.jpg', '.jpeg']:
#             #TODO consider using magic bytes to ID files better
#             if self.original_file.endswith(fmat):
#                 return True
#         return False
#
#     def is_gif(self):
#         #TODO consider using magic bytes to ID files better
#         if self.original_file.endswith('.gif'):
#             return True
#         return False
#
#     def is_animated(self):
#         im = Image.open(self.original_file)
#         try:
#             im.seek(1)
#         except EOFError:
#             pass
#         else:
#             self.is_animated = True
#
#     def fix_image(self):
#         if self.is_jpeg():
#             #open with PIL and save as BMP
#             im = Image.open(self.original_file)
#             new_file = self.original_file.rsplit('.', 1)[0] + '.bmp'
#             im.save(new_file)
#             self.fixed_file = new_file
#         else:
#             return
#
#     def new(self, width, height, color="black"):
#         """Initializes the video object as a new video"""
#         self.prevent_multiple_initializations()
#         image = Image.new("RGB", (width, height), color)
#         image.save('%s.bmp' % self.temp_file)
#         self.initialized = True
#
#     def open(self, asset):
#         """Initializes the video object using an existing asset"""
#         self.prevent_multiple_initializations()
#         self.check_exists(asset)
#         if self.is_image():
#             self.fix_image()