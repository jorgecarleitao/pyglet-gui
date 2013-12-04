from setup import *

from pyglet_gui.gui import PopupMessage

# Set up a Dialog
dialog = PopupMessage(text="Test",
                      window=window,
                      batch=batch,
                      theme=theme)

pyglet.app.run()
