from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.option_selectors import VerticalButtonSelector

# Set up a Dialog
dialog = Dialog(VerticalButtonSelector(options=["Option %d" % x for x in range(1, 6)]),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
