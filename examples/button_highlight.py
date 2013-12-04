from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.mixins import HighlightMixin
from pyglet_gui.dialog import Dialog


class HighlightedButton(Button, HighlightMixin):
    """
    An example of a Button that changes behavior when is mouse-hovered.
    We mix the behavior of button with the HighlightMixin.
    """
    def __init__(self, text, is_pressed=False, on_press=None):
        Button.__init__(self, text, is_pressed, on_press)
        HighlightMixin.__init__(self)

    def load(self):
        super().load()
        HighlightMixin.load(self)

    def layout(self):
        super().layout()
        HighlightMixin.layout(self)

    def unload(self):
        Button.unload(self)
        HighlightMixin.unload(self)

# Set up a Dialog
dialog = Dialog(HighlightedButton("Button"),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
