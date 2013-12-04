from setup import *
from pyglet_gui.buttons import Button

from pyglet_gui.dialog import Dialog
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalLayout
from pyglet_gui.sliders import HorizontalSlider


# Set up a Dialog
dialog = Dialog(
    # an horizontal layout with two vertical layouts, each one with a slider.
    Scrollable(height=100, width=200, content=VerticalLayout(content=[Button(str(x)) for x in range(10)])),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
