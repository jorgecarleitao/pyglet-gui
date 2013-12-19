from setup import *

from pyglet_gui.gui import PopupMessage
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
