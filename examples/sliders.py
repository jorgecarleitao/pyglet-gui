from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import VerticalLayout
from pyglet_gui.sliders import HorizontalSlider

# Set up a Dialog
dialog = Dialog(
    VerticalLayout([HorizontalSlider(), HorizontalSlider(steps=10)]),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
