from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.widgets import Label
from pyglet_gui.gui import Frame
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "frame": {
                   "image": {
                       "source": "panel.png",
                       "frame": [8, 8, 16, 16],
                       "padding": [16, 16, 8, 8]
                   }
               }
              }, resources_path='../theme/')

dialog = Dialog(Frame(Label('An example of a white label with a red frame')),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
