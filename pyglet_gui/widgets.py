from pyglet_gui.core import Widget
import pyglet.text


class Spacer(Widget):
    def __init__(self, min_width=0, min_height=0):
        Widget.__init__(self)
        self._min_width, self._min_height = min_width, min_height

    def expand(self, width, height):
        self.width, self.height = width, height

    def is_expandable(self):
        return True

    def compute_size(self):
        return self._min_width, self._min_height


class Graphic(Widget):
    def __init__(self, path, is_expandable=False):
        Widget.__init__(self)
        self._path = path
        self._expandable = is_expandable
        self._graphic = None
        self._min_width = self._min_height = 0

    def get_path(self):
        return self._path

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self._graphic = theme['image'].generate(theme[self._path]['gui_color'], **self.get_batch('background'))

        self._min_width = self._graphic.width
        self._min_height = self._graphic.height

    def unload_graphics(self):
        self._graphic.unload()

    def expand(self, width, height):
        assert self._expandable
        self.width, self.height = width, height
        self._graphic.update(self.x, self.y, self.width, self.height)

    def is_expandable(self):
        return self._expandable

    def layout(self):
        self._graphic.update(self.x, self.y, self.width, self.height)

    def compute_size(self):
        return self._min_width, self._min_height


class Label(Widget):
    def __init__(self, text="", bold=False, italic=False,
                 font_name=None, font_size=None, color=None, path=None):
        Widget.__init__(self)
        self.text = text
        self.bold = bold
        self.italic = italic
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.path = path
        self.label = None

    def get_path(self):
        return self.path

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self.label = pyglet.text.Label(self.text,
                                       bold=self.bold,
                                       italic=self.italic,
                                       color=self.color or theme['text_color'],
                                       font_name=self.font_name or theme['font'],
                                       font_size=self.font_size or theme['font_size'],
                                       **self.get_batch('background'))

    def unload_graphics(self):
        self.label.delete()

    def layout(self):
        font = self.label.document.get_font()
        self.label.x = self.x
        self.label.y = self.y - font.descent

    def set_text(self, text):
        self.text = text
        self.reload()
        self.reset_size()

    def compute_size(self):
        font = self.label.document.get_font()
        return self.label.content_width, font.ascent - font.descent
