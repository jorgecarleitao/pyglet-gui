from setup import *

from pyglet_gui.gui import PopupMessage
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
                "frame": [6, 6, 3, 3],
                "padding": [12, 12, 4, 2]
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
                "frame": [6, 6, 3, 3],
                "padding": [12, 12, 4, 2]
            }
        },
    },
    "frame": {
        "image": {
            "source": "panel.png",
            "frame": [8, 8, 16, 16],
            "padding": [16, 16, 8, 8]
            }
        }
}, resources_path='../theme/')

# Set up a Manager
PopupMessage(text="Test",
             window=window,
             batch=batch,
             theme=theme)

pyglet.app.run()
