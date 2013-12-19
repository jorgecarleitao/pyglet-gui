from pyglet_gui.manager import Manager
from setup import *

from pyglet_gui.document import Document
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [64, 64, 64, 255],
               "vscrollbar": {
                   "knob": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 16, 16, 16],
                           "frame": [0, 6, 16, 4],
                           "padding": [0, 0, 0, 0]
                       },
                       "offset": [0, 0]
                   },
                   "bar": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 64, 16, 16]
                       },
                       "padding": [0, 0, 0, 0]
                   }
               }
              }, resources_path='../theme')

document = pyglet.text.decode_attributed('''
In {bold True}Pyglet-gui{bold False} you can use
{underline (255, 255, 255, 255)}pyglet{underline None}'s documents in a
scrollable window.

You can also {font_name "Courier New"}change fonts{font_name Lucia Grande},
{italic True}italicize your text{italic False} and use all features of Pyglet's document.
''')

# Set up a Manager
Manager(Document(document, width=300, height=50),
        window=window, batch=batch, group=fg_group,
        theme=theme)

pyglet.app.run()
