from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.mixins import FocusMixin
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import VerticalLayout
from pyglet_gui.widgets import Label


class FocusButton(Button, FocusMixin):
    """
    An example of a Button that is focusable and thus can be selected with TAB.
    """
    def __init__(self, text, is_pressed=False, on_press=None):
        Button.__init__(self, text, is_pressed, on_press)
        FocusMixin.__init__(self)

    def load(self):
        super().load()
        FocusMixin.load(self)

    def layout(self):
        super().layout()
        FocusMixin.layout(self)

    def unload(self):
        super().unload()
        FocusMixin.unload(self)

    def on_key_press(self, symbol, modifiers):
        # button also changes state on ENTER.
        if symbol == pyglet.window.key.ENTER:
            self.change_state()


# Set up a Dialog
dialog = Dialog(VerticalLayout([Label("Try (SHIFT+)TAB and ENTER"),
                                FocusButton("Button 1"),
                                FocusButton("Button 2"),
                                FocusButton("Button 3")]),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
