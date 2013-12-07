from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.mixins import HighlightMixin
from pyglet_gui.dialog import Dialog
from pyglet_gui.theme import Theme

theme = Theme({
    "font": "Lucida Grande",
    "font_size": 12,
    "font_size_small": 10,
    "gui_color": [255, 255, 255, 255],
    "disabled_color": [160, 160, 160, 255],
    "text_color": [255, 255, 255, 255],
    "highlight_color": [255, 255, 255, 64],
    "button": {
        "down": {
            "highlight": {
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
            "highlight": {
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


class HighlightedButton(Button, HighlightMixin):
    """
    An example of a Button that changes behavior when is mouse-hovered.
    We mix the behavior of button with HighlightMixin.
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
