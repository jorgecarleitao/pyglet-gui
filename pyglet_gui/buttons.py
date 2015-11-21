import pyglet.window

from pyglet_gui.override import Label
from pyglet_gui.constants import HALIGN_LEFT, HALIGN_RIGHT

from pyglet_gui.controllers import TwoStateController
from pyglet_gui.core import Viewer
from pyglet_gui.mixins import FocusMixin

class Button(TwoStateController, Viewer):
    def __init__(self, label="", is_pressed=False, on_press=None):
        TwoStateController.__init__(self, is_pressed=is_pressed, on_press=on_press)
        Viewer.__init__(self)

        self.label = label

        # graphics
        self._label = None
        self._button = None

    def change_state(self):
        self._is_pressed = not self._is_pressed
        self.reload()
        self.reset_size()
        self._on_press(self._is_pressed)

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.change_state()

    def get_path(self):
        path = ['button']
        if self.is_pressed:
            path.append('down')
        else:
            path.append('up')
        return path

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self._button = theme['image'].generate(theme['gui_color'], **self.get_batch('background'))

        self._label = Label(self.label,
                            font_name=theme['font'],
                            font_size=theme['font_size'],
                            color=theme['text_color'],
                            **self.get_batch('foreground'))

    def unload_graphics(self):
        self._button.unload()
        self._label.unload()

    def compute_size(self):
        # Treat the height of the label as ascent + descent
        font = self._label.document.get_font()
        height = font.ascent - font.descent

        return self._button.get_needed_size(self._label.content_width, height)

    def layout(self):
        self._button.update(self.x, self.y, self.width, self.height)

        # centers the label on the middle of the button
        x, y, width, height = self._button.get_content_region()

        font = self._label.document.get_font()
        self._label.x = x + width/2 - self._label.content_width/2
        self._label.y = y + height/2 - font.ascent/2 - font.descent
        self._label.update()

    def delete(self):
        TwoStateController.delete(self)
        Viewer.delete(self)


class GroupButton(Button):
    button_groups = {}

    def __init__(self, group_id="", label="", is_pressed=False, on_press=None):
        Button.__init__(self, label=label, is_pressed=is_pressed, on_press=on_press)
        self.button_groups.setdefault(group_id, []).append(self)
        self.group_id = group_id

    def change_state(self):
        for button in self.button_groups[self.group_id]:
            if button._is_pressed and button is not self:
                button.change_state()
        super(GroupButton, self).change_state()


class OneTimeButton(Button):
    def __init__(self, label="", on_release=None):
        Button.__init__(self, label=label)

        self.on_release = lambda x: x
        if on_release is not None:
            self.on_release = on_release

    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_pressed:
            self.change_state()

            # If mouse is still hovering us, signal on_release
            if self.hit_test(x, y):
                self.on_release(self._is_pressed)


class Checkbox(Button):
    def __init__(self, label="", is_pressed=False, on_press=None, align=HALIGN_RIGHT, padding=4):

        assert align in [HALIGN_LEFT, HALIGN_RIGHT]
        Button.__init__(self, label=label, is_pressed=is_pressed, on_press=on_press)

        self.align = align  # where the label is positioned.

        # private
        self._padding = padding

    def get_path(self):
        path = ['checkbox']
        if self.is_pressed:
            path.append('checked')
        else:
            path.append('unchecked')
        return path

    def layout(self):
        if self.align == HALIGN_RIGHT:  # label goes on right
            self._button.update(self.x,
                                self.y + self.height/2 - self._button.height/2,
                                self._button.width,
                                self._button.height)
            self._label.x = self.x + self._button.width + self._padding
        else:  # label goes on left
            self._label.x = self.x
            self._button.update(self.x + self._label.content_width + self._padding,
                                self.y + self.height/2 - self._button.height/2,
                                self._button.width,
                                self._button.height)

        font = self._label.document.get_font()
        height = font.ascent - font.descent
        self._label.y = self.y + self.height/2 - height/2 - font.descent

    def compute_size(self):
        # Treat the height of the label as ascent + descent
        font = self._label.document.get_font()
        height = font.ascent - font.descent

        return self._button.width + self._padding + self._label.content_width, max(self._button.height, height)


class FocusButton(Button, FocusMixin):
    """
    Button that is focusable and thus can be selected with TAB.
    """
    def __init__(self, label="", is_pressed=False, on_press=None):
        Button.__init__(self, label, is_pressed, on_press)
        FocusMixin.__init__(self)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.change_state()
