import pyglet
from pyglet_gui.mixins import FocusMixin
from pyglet_gui.override import InputLabel
from pyglet_gui.widgets import Widget


class TextInput(FocusMixin, Widget):
    # This class works in two states defined by is_focus():
    #   True: "writing"
    #   False: "label"

    def __init__(self, text="", length=20, max_length=None, padding=0, on_input=None):
        Widget.__init__(self)
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
        assert self._text_layout is None and self._caret is None
        if self._label is None:
            self._label = InputLabel(self._document.text,
                                     multiline=False,
                                     width=self.width-self._padding*2,
                                     color=theme['text_color'], **self.get_batch('foreground'))

    def _load_writing(self, theme):
        assert self._label is None
        needed_width, needed_height = self._compute_needed_size()
        if self._text_layout is None:
            self._text_layout = pyglet.text.layout.IncrementalTextLayout(
                self._document, needed_width, needed_height,
                multiline=False, **self.get_batch('foreground'))
            assert self._caret is None
        if self._caret is None:
            self._caret = pyglet.text.caret.Caret(self._text_layout, color=theme['gui_color'][0:3])
            self._caret.visible = True
            self._caret.mark = 0
            self._caret.position = len(self._document.text)

    def load_graphics(self):
        FocusMixin.load_graphics(self)
        theme = self.theme[self.get_path()]

        # We set the style once. We shouldn't have to do so again because
        # it's an UnformattedDocument.
        if not self._document_style_set:
            self._document.set_style(0, 0,  # parameters not used in set_style
                                     dict(color=theme['text_color'],
                                          font_name=theme['font'],
                                          font_size=theme['font_size']))
            self._document_style_set = True

        if self.is_focus():
            self._load_writing(theme)
        else:
            self._load_label(theme)

        if self._field is None:
            color = theme['gui_color']
            self._field = theme['image'].generate(color=color, **self.get_batch('background'))

    def unload_graphics(self):
        if self._caret is not None:
            self._caret.delete()
            self._caret = None
        if self._text_layout is not None:
            self._document.remove_handlers(self._text_layout)
            self._text_layout.delete()
            self._text_layout = None
        if self._label is not None:
            self._label.delete()
            self._label = None
        if self._field is not None:
            self._field.unload()
            self._field = None

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
        Widget.layout(self)
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
        FocusMixin.on_gain_focus(self)

        self.reload()
        self.reset_size()
        self.layout()

    def on_lose_focus(self):
        FocusMixin.on_lose_focus(self)
        if self._on_input is not None:
            self._on_input(self.get_text())

        self.reload()
        self.reset_size()
        self.layout()

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._caret is not None:
            return self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._caret is not None:
            return self._caret.on_mouse_press(x, y, button, modifiers)

    def on_text(self, text):
        assert self._caret is not None

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
        if self._caret:
            self._caret.mark = self._caret.position = len(self._document.text)
        elif self._label:
            self._label.text = text

    def compute_size(self):
        needed_width, needed_height = self._compute_needed_size()
        return self._field.get_needed_size(needed_width, needed_height)

    def delete(self):
        Widget.delete(self)
        FocusMixin.delete(self)
