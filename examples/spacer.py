from setup import *

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button
from pyglet_gui.containers import HorizontalContainer, VerticalContainer, Spacer
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

# First line has two big buttons
# second line has three spacers, separated by two small buttons.
# size of the three spacers is the same.
Manager(VerticalContainer([HorizontalContainer([Button(label="Big fat button"),
                                                Button(label="Big fat button")], padding=0),

                           HorizontalContainer([Spacer(),
                                                Button(label="Small"),
                                                Spacer(),
                                                Button(label="Small"),
                                                Spacer()], padding=0)],
                          padding=0),
        window=window,
        batch=batch,
        theme=theme)

pyglet.app.run()
