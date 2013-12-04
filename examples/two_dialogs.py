from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.buttons import Button
from pyglet_gui.constants import ANCHOR_TOP_LEFT

# Set up a Dialog
dialog1 = Dialog(Button("Test 1"), window=window,
                 batch=batch,
                 group=fg_group,
                 theme=theme)

dialog2 = Dialog(Button("Test 2"), window=window,
                 batch=batch,
                 group=fg_group,
                 anchor=ANCHOR_TOP_LEFT,
                 theme=theme)



pyglet.app.run()
