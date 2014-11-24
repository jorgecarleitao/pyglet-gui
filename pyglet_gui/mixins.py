from pyglet_gui.core import Controller
from pyglet_gui.core import Viewer


class HighlightMixin(Controller, Viewer):
    def __init__(self):
        Viewer.__init__(self)
        Controller.__init__(self)
        self._highlight = None
        self._highlight_flag = False

    def on_gain_highlight(self):
        self._highlight_flag = True
        HighlightMixin.load_graphics(self)
        HighlightMixin.layout(self)

    def on_lose_highlight(self):
        self._highlight_flag = False
        HighlightMixin.unload_graphics(self)

    def is_highlighted(self):
        return self._highlight_flag

    def load_graphics(self):
        theme = self.theme[self.get_path()]
        if self._highlight is None and self._highlight_flag:
            self._highlight = theme['highlight']['image'].generate(theme['highlight_color'],
                                                                   **self.get_batch('highlight'))

    def unload_graphics(self):
        if self._highlight is not None:
            self._highlight.unload()
            self._highlight = None

    def layout(self):
        if self._highlight is not None:
            self._highlight.update(self.x, self.y, self.width, self.height)

    def delete(self):
        HighlightMixin.unload_graphics(self)


class FocusMixin(Controller, Viewer):
    def __init__(self):
        Controller.__init__(self)
        Viewer.__init__(self)
        self._focus = None
        self._focus_flag = False

    def on_gain_focus(self):
        self._focus_flag = True
        FocusMixin.load_graphics(self)
        FocusMixin.layout(self)
        return True

    def on_lose_focus(self):
        self._focus_flag = False
        FocusMixin.unload_graphics(self)
        return True

    def is_focus(self):
        return self._focus_flag

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self._focus = theme['focus']['image'].generate(theme['focus_color'], **self.get_batch('highlight'))

    def unload_graphics(self):
        self._focus.unload()
        self._focus = None

    def layout(self):
        if self._focus is not None:
            self._focus.update(self.x, self.y, self.width, self.height)

    def delete(self):
        if self._focus is not None:
            FocusMixin.unload_graphics(self)
