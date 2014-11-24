import pyglet
from pyglet_gui.mixins import FocusMixin
from pyglet_gui.override import InputLabel
from pyglet_gui.core import Viewer


class TextInput(FocusMixin, Viewer):
    # This class works in two states defined by is_focus():
    #   True: "writing"
    #   False: "label"

    def __init__(self, text="", length=20, max_length=None, padding=0, on_input=None):
        Viewer.__init__(self)
        FocusMixin.__init__(self)

        self._document = pyglet.text.document.UnformattedDocument(text)
        self._document_style_set = False  # check if style of document was set.

        self._length = length  # the length of the box in characters
        self._max_length = max_length  # the max length allowed for writing.
        self._on_input = on_input

        self._padding = 4 + padding

        # graphics loaded in both states
        self._field = None

        # graphics loaded in state "writing"
        self._text_layout = None
        self._caret = None

        # graphics loaded in state "label"
        self._label = None

    def get_path(self):
        return 'input'

    def _load_label(self, theme):
        self._label = InputLabel(self._document.text,
                                 multiline=False,
                                 width=self.width-self._padding*2,
                                 color=theme['text_color'],
                                 font_name=theme['font'],
                                 font_size=theme['font_size'],
                                 **self.get_batch('foreground'))

    def _load_writing(self, theme):
        needed_width, needed_height = self._compute_needed_size()

        self._text_layout = pyglet.text.layout.IncrementalTextLayout(
            self._document, needed_width, needed_height,
            multiline=False, **self.get_batch('foreground'))

        self._caret = pyglet.text.caret.Caret(self._text_layout, color=theme['gui_color'][0:3])
        self._caret.visible = True
        self._caret.mark = 0
        self._caret.position = len(self._document.text)

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        # We set the style once. We shouldn't have to do so again because
        # it's an UnformattedDocument.
        if not self._document_style_set:
            self._document.set_style(0, 0,  # parameters not used in set_style
                                     dict(color=theme['text_color'],
                                          font_name=theme['font'],
                                          font_size=theme['font_size']))
            self._document_style_set = True

        self._field = theme['image'].generate(color=theme['gui_color'], **self.get_batch('background'))
        if self.is_focus():
            self._load_writing(theme)
        else:
            self._load_label(theme)

    def _unload_writing(self):
        self._caret.delete()  # it should be .unload(), but Caret does not have it.
        self._document.remove_handlers(self._text_layout)
        self._text_layout.delete()  # it should also be .unload().
        self._caret = self._text_layout = None

    def _unload_label(self):
        self._label.delete()
        self._label = None

    def unload_graphics(self):
        if self.is_focus():
            self._unload_writing()
        else:
            self._unload_label()

        self._field.unload()

    def _compute_needed_size(self):
        # Calculate the needed size based on the font size
        font = self._document.get_font(0)
        height = font.ascent - font.descent
        glyphs = font.get_glyphs('A_')
        width = max([x.width for x in glyphs])
        needed_width = self._length * width - 2 * self._padding
        needed_height = height + 2 * self._padding
        return needed_width, needed_height

    def get_text(self):
        return self._document.text

    def layout(self):
        Viewer.layout(self)
        self._field.update(self.x, self.y, self.width, self.height)

        x, y, width, height = self._field.get_content_region()
        if self.is_focus():
            self._text_layout.begin_update()
            self._text_layout.x = self.x + self._padding
            self._text_layout.y = self.y - self._padding
            self._text_layout.end_update()
        else:
            # Adjust the text for font's descent
            descent = self._document.get_font().descent
            self._label.begin_update()
            self._label.x = self.x + self._padding
            self._label.y = self.y + self._padding - descent
            self._label.width = width - self._padding * 2
            self._label.end_update()

    def on_gain_focus(self):
        self.unload()
        FocusMixin.on_gain_focus(self)  # changes is_focus()
        self.load()

        self.reset_size()
        self.layout()

    def on_lose_focus(self):
        # send text to callback _on_input
        if self._on_input is not None:
            self._on_input(self.get_text())

        self.unload()
        FocusMixin.on_lose_focus(self)  # changes is_focus()
        self.load()

        self.reset_size()
        self.layout()

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.is_focus():
            return self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_focus():
            return self._caret.on_mouse_press(x, y, button, modifiers)

    def on_text(self, text):
        assert self.is_focus()

        self._caret.on_text(text)
        if self._max_length and len(self._document.text) > self._max_length:
            self._document.text = self._document.text[:self._max_length]
            self._caret.mark = self._caret.position = self._max_length
        return pyglet.event.EVENT_HANDLED

    def on_text_motion(self, motion):
        assert self.is_focus()
        return self._caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        assert self.is_focus()
        return self._caret.on_text_motion_select(motion)

    def set_text(self, text):
        self._document.text = text
        if self.is_focus():
            self._caret.mark = self._caret.position = len(self._document.text)
        else:
            self._label.text = text

    def compute_size(self):
        needed_width, needed_height = self._compute_needed_size()
        return self._field.get_needed_size(needed_width, needed_height)

    def delete(self):
        FocusMixin.delete(self)
        Viewer.delete(self)
