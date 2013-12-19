from pyglet_gui.manager import Manager
from setup import *

from pyglet_gui.containers import VerticalContainer
from pyglet_gui.sliders import HorizontalSlider
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "slider": {
                   "knob": {
                       "image": {
                           "source": "slider-knob.png"
                       },
                       "offset": [-5, -11]
                   },
                   "padding": [8, 8, 8, 8],
                   "step": {
                       "image": {
                           "source": "slider-step.png"
                       },
                       "offset": [-2, -8]
                   },
                   "bar": {
                       "image": {
                           "source": "slider-bar.png",
                           "frame": [8, 8, 8, 0],
                           "padding": [8, 8, 8, 8]
                       }
                   }
               }
              }, resources_path='../theme/')


# Set up a Manager
dialog = Manager(
    VerticalContainer([HorizontalSlider(), HorizontalSlider(steps=10)]),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
