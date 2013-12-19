from pyglet_gui.manager import Manager
from setup import *

from pyglet_gui.buttons import Button
from pyglet_gui.containers import VerticalContainer, HorizontalContainer, GridContainer
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


hlay = HorizontalContainer(content=[VerticalContainer(content=[Button("(1,1)"), Button("(1,2)")]),
                                 VerticalContainer(content=[Button("(2,1)"), Button("(2,2)")])])

grid = GridContainer([[Button("(1,1)"), Button("(1,2)")],
                   [Button("(2,1)"), Button("(2,2)")]])

vlay = VerticalContainer([hlay, grid])

Manager(vlay, window=window, batch=batch, theme=theme)

pyglet.app.run()
