from pyglet_gui.core import Viewer
import pyglet.text


class Rectangle():
    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self.width = width
        self.height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def is_inside(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


class Widget(Rectangle, Viewer):
    def __init__(self, width=0, height=0):
        Rectangle.__init__(self, 0, 0, width, height)
        Viewer.__init__(self)

    def set_position(self, x, y):
        super().set_position(x, y)
        self.layout()

    def get_path(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def unload(self):
        raise NotImplementedError

    def layout(self):
        pass

    def compute_size(self):
        raise NotImplementedError(self)

    def reset_size(self, reset_parent=True):
        width, height = self.compute_size()

        # we only reset the parent if we change size
        changed = False
        if self.width != width or self.height != height:
            self.width, self.height = width, height
            changed = True
        self.layout()
        # we only reset parent if the parent exists and
        # the flag to reset it is set.
        if changed and reset_parent:
            self.parent.reset_size(reset_parent)


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

    def load(self):
        theme = self.theme[self.get_path()]
        if self._graphic is None:
            template = theme['image']
            self._graphic = template.generate(theme[self._path]['gui_color'], **self.get_batch('background'))
            self._min_width = self._graphic.width
            self._min_height = self._graphic.height

    def unload(self):
        if self._graphic is not None:
            self._graphic.unload()
            self._graphic = None

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

    def load(self):
        theme = self.theme[self.get_path()]
        if self.label is None:
            self.label = pyglet.text.Label(self.text,
                                           bold=self.bold,
                                           italic=self.italic,
                                           color=self.color or theme['gui_color'],
                                           font_name=self.font_name or theme['font'],
                                           font_size=self.font_size or theme['font_size'],
                                           **self.get_batch('background'))

    def unload(self):
        if self.label is not None:
            self.label.delete()
            self.label = None

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
