from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.text_input import TextInput
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "input": {
                   "image": {
                       "source": "input.png",
                       "frame": [3, 3, 2, 2],
                       "padding": [3, 3, 2, 3]
                   },
                   # need a focus color
                   "focus_color": [255, 255, 255, 64],
                   "focus": {
                       "image": {
                           "source": "input-highlight.png"
                       }
                   }
               }
              }, resources_path='../theme/')

# Set up a Dialog
dialog = Dialog(TextInput(text="Write on me"),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
