from setup import *

from pyglet_gui.buttons import Button, OneTimeButton, Checkbox
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import VerticalLayout


# Set up a Dialog
dialog = Dialog(VerticalLayout([Button("Button"),
                                OneTimeButton("OneTimeButton"),
                                Checkbox("Checkbox")]),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
