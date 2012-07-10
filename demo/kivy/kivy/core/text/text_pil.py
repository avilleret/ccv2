'''
Text PIL: Draw text with PIL
'''

__all__ = ('LabelPIL', )

try:
    from PIL import Image, ImageFont, ImageDraw
except:
    raise

import os
from . import LabelBase
from kivy import kivy_data_dir
from kivy.core.image import ImageData

# used for fetching extends before creature image surface
default_font = ImageFont.load_default()


class LabelPIL(LabelBase):
    _cache = {}

    def _select_font(self):
        fontsize = int(self.options['font_size'] * 1.333)
        fontname = self.options['font_name'].split(',')[0]
        id = '%s.%s' % (unicode(fontname), unicode(fontsize))
        if not id in self._cache:
            filename = os.path.join(kivy_data_dir, 'DejaVuSans.ttf')
            font = ImageFont.truetype(filename, fontsize)
            self._cache[id] = font

        return self._cache[id]

    def get_extents(self, text):
        font = self._select_font()
        w, h = font.getsize(text)
        return w, h

    def _render_begin(self):
        # create a surface, context, font...
        self._pil_im = Image.new('RGBA', self._size)
        self._pil_draw = ImageDraw.Draw(self._pil_im)

    def _render_text(self, text, x, y):
        self._pil_draw.text((int(x), int(y)),
            text, font=self._select_font(), fill=(255, 255, 255, 255))

    def _render_end(self):
        data = ImageData(self._size[0], self._size[1],
                         self._pil_im.mode.lower(), self._pil_im.tostring())

        del self._pil_im
        del self._pil_draw

        return data