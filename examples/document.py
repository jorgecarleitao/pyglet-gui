from setup import *

from pyglet_gui.document import Document
from pyglet_gui.dialog import Dialog

document = pyglet.text.decode_attributed('''
In {bold True}pyglet_gui{bold False} you can use
{underline (255, 255, 255, 255)}pyglet{underline None}'s documents in a
scrollable window.

You can also {font_name "Courier New"}change fonts{font_name Lucia Grande},
{italic True}italicize your text{italic False}, and more.
''')

# Set up a Dialog
dialog = Dialog(
    Document(document, width=300, height=50),
    window=window, batch=batch, group=fg_group,
    theme=theme)

pyglet.app.run()
