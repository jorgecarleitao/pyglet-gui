from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.text_input import TextInput

# Set up a Dialog
dialog = Dialog(TextInput(text="Write on me"),
                window=window,
                batch=batch,
                theme=theme)

pyglet.app.run()
