from pyglet_gui.manager import Manager
from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.mixins import HighlightMixin
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

    def load_graphics(self):
        super().load_graphics()
        HighlightMixin.load_graphics(self)

    def layout(self):
        super().layout()
        HighlightMixin.layout(self)

    def unload_graphics(self):
        Button.unload_graphics(self)
        HighlightMixin.unload_graphics(self)

# Set up a Manager
dialog = Manager(HighlightedButton("Button"),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
