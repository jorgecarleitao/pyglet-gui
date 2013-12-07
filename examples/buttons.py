from setup import *

from pyglet_gui.buttons import Button, OneTimeButton, Checkbox
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import VerticalLayout
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "button": {
                   "down": {
                       "image": {
                           "source": "button-down.png",
                           "frame": [8, 6, 2, 2],
                           "padding": [18, 18, 8, 6]
                       },
                       "text_color": [0, 0, 0, 255]
                   },
                   "up": {
                       "image": {
                           "source": "button.png",
                           "frame": [6, 5, 6, 3],
                           "padding": [18, 18, 8, 6]
                       }
                   }
               },
               "checkbox": {
                   "checked": {
                       "image": {
                           "source": "checkbox-checked.png"
                       }
                   },
                   "unchecked": {
                       "image": {
                           "source": "checkbox.png"
                       }
                   }
               }
              }, resources_path='../theme/')

# Set up a Dialog
dialog = Dialog(VerticalLayout([Button(label="Persistent button"),
                                OneTimeButton(label="One time button"),
                                Checkbox(label="Checkbox")]),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
