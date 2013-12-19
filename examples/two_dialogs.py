from pyglet_gui.gui import Label
from pyglet_gui.manager import Manager
from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.constants import ANCHOR_TOP_LEFT
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
               }
               }, resources_path='../theme/')


# Set up a Manager
dialog1 = Manager(Label("Drag me"), window=window,
                 batch=batch,
                 group=fg_group,
                 theme=theme)

dialog2 = Manager(Button("Drag me"), window=window,
                 batch=batch,
                 group=fg_group,
                 anchor=ANCHOR_TOP_LEFT,
                 theme=theme)

pyglet.app.run()
