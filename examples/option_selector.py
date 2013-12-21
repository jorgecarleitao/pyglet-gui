from setup import *

from pyglet_gui.manager import Manager
from pyglet_gui.option_selectors import VerticalButtonSelector
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
Manager(VerticalButtonSelector(options=["Option %d" % x for x in range(1, 6)]),
        window=window,
        batch=batch,
        theme=theme)

pyglet.app.run()
