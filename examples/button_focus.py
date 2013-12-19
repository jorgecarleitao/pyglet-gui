from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.mixins import FocusMixin
from pyglet_gui.gui import Label
from pyglet_gui.manager import Manager
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme

theme = Theme({
    "font": "Lucida Grande",
    "font_size": 12,
    "font_size_small": 10,
    "gui_color": [255, 255, 255, 255],
    "disabled_color": [160, 160, 160, 255],
    "text_color": [255, 255, 255, 255],
    "focus_color": [255, 255, 255, 64],
    "button": {
        "down": {
            "focus": {
                "image": {
                    "source": "button-highlight.png",
                    "frame": [8, 6, 2, 2],
                    "padding": [18, 18, 8, 6]
                }
            },
            "image": {
                "source": "button-down.png",
                "frame": [8, 6, 2, 2],
                "padding": [18, 18, 8, 6]
            },
            "text_color": [0, 0, 0, 255]
        },
        "up": {
            "focus": {
                "image": {
                    "source": "button-highlight.png",
                    "frame": [8, 6, 2, 2],
                    "padding": [18, 18, 8, 6]
                }
            },
            "image": {
                "source": "button.png",
                "frame": [6, 5, 6, 3],
                "padding": [18, 18, 8, 6]
            }
        }
    }}, resources_path='../theme/')


class FocusButton(Button, FocusMixin):
    """
    An example of a Button that is focusable and thus can be selected with TAB.
    """
    def __init__(self, text, is_pressed=False, on_press=None):
        Button.__init__(self, text, is_pressed, on_press)
        FocusMixin.__init__(self)

    def load_graphics(self):
        super().load_graphics()
        FocusMixin.load_graphics(self)

    def layout(self):
        super().layout()
        FocusMixin.layout(self)

    def unload_graphics(self):
        super().unload_graphics()
        FocusMixin.unload_graphics(self)

    def on_key_press(self, symbol, modifiers):
        # button also changes state on ENTER.
        if symbol == pyglet.window.key.ENTER:
            self.change_state()


# Set up a Manager
dialog = Manager(VerticalContainer([Label("Try (SHIFT+)TAB and ENTER"),
                                FocusButton("Button 1"),
                                FocusButton("Button 2"),
                                FocusButton("Button 3")]),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
