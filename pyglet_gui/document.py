import pyglet

from pyglet_gui.scrollbars import VScrollbar
from pyglet_gui.core import Viewer, Rectangle
from pyglet_gui.controllers import Controller


class Document(Controller, Viewer):
    """
    Allows you to embed a document within the GUI, which includes a
    vertical scrollbar.
    """
    def __init__(self, document, width=0, height=0, is_fixed_size=False):
        Viewer.__init__(self, width, height)
        Controller.__init__(self)

        self.max_height = height
        if isinstance(document, str):
            self._document = pyglet.text.document.UnformattedDocument(document)
        else:
            self._document = document
        self._content = None
        self.content_width = width
        self._scrollbar = None
        self.set_document_style = False
        self.is_fixed_size = is_fixed_size

    def hit_test(self, x, y):
        if self._content is not None:
            return Rectangle(self._content.x,
                             self._content.y,
                             self._content.width,
                             self._content.height).is_inside(x, y)
        else:
            return False

    def _load_scrollbar(self, height):
        if self._content.content_height > height:
            if self._scrollbar is None:
                self._scrollbar = VScrollbar(self.max_height)
                self._scrollbar.set_manager(self._manager)
                self._scrollbar.parent = self
                self._scrollbar.load()
                self._scrollbar.set_knob_size(self.height, self._content.content_height)
        # if smaller, we unload it if it is loaded
        elif self._scrollbar is not None:
            self._scrollbar.unload()
            self._scrollbar = None

    def load_graphics(self):
        if not self.set_document_style:
            self.do_set_document_style(self._manager)

        self._content = pyglet.text.layout.IncrementalTextLayout(self._document,
                                                                 self.content_width, self.max_height,
                                                                 multiline=True, **self.get_batch('background'))

    def unload_graphics(self):
        self._content.delete()
        if self._scrollbar is not None:
            self._scrollbar.unload()
            self._scrollbar = None

    def do_set_document_style(self, dialog):
        self.set_document_style = True

        # Check the style runs to make sure we don't stamp on anything
        # set by the user
        self._do_set_document_style('color', dialog.theme['text_color'])
        self._do_set_document_style('font_name', dialog.theme['font'])
        self._do_set_document_style('font_size', dialog.theme['font_size'])

    def _do_set_document_style(self, attr, value):
        length = len(self._document.text)
        runs = [(start, end, doc_value) for start, end, doc_value in
                self._document.get_style_runs(attr).ranges(0, length)
                if doc_value is not None]
        if not runs:
            terminator = len(self._document.text)
        else:
            terminator = runs[0][0]
        self._document.set_style(0, terminator, {attr: value})

    def get_text(self):
        return self._document.text

    def layout(self):
        if self._scrollbar is not None:
            self._scrollbar.set_position(self.x + self._content.content_width, self.y)
            pos = self._scrollbar.get_knob_pos()
            if pos != -self._content.view_y:
                self._content.view_y = -pos

        self._content.begin_update()
        self._content.x = self.x
        self._content.y = self.y
        self._content.end_update()

        if self._scrollbar is not None:
            self._scrollbar.set_position(self.x + self.content_width, self.y)

    def on_gain_highlight(self):
        if self._scrollbar is not None:
            self._manager.set_wheel_target(self._scrollbar)

    def on_lose_highlight(self):
        self._manager.set_wheel_target(None)

    def compute_size(self):
        if self.is_fixed_size or (self.max_height and self._content.content_height > self.max_height):
            height = self.max_height
        else:
            height = self._content.content_height
        self._content.height = height

        self._load_scrollbar(height)
        if self._scrollbar is not None:
            self._scrollbar.set_knob_size(height, self._content.content_height)
            self._scrollbar.compute_size()
            width = self.content_width + self._scrollbar.width
        else:
            width = self.content_width

        return width, height

    def set_text(self, text):
        self._document.text = text
        self.compute_size()
        self.layout()

    def delete(self):
        Controller.delete(self)
        Viewer.delete(self)
