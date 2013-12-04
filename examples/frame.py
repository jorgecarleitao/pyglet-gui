from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.widgets import Label
from pyglet_gui.containers import Frame


dialog = Dialog(Frame(Label('Test')),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
