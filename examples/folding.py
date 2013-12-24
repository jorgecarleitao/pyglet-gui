from setup import *

from pyglet_gui.manager import Manager
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.document import Document
from pyglet_gui.constants import ANCHOR_CENTER, HALIGN_LEFT
from pyglet_gui.gui import SectionHeader, FoldingSection, Frame
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "section": {
                   "right": {
                       "image": {
                           "source": "line.png",
                           "region": [2, 0, 6, 4],
                           "frame": [0, 4, 4, 0],
                           "padding": [0, 0, 0, 6]
                       }
                   },
                   "font_size": 14,
                   "opened": {
                       "image": {
                           "source": "book-open.png"
                       }
                   },
                   "closed": {
                       "image": {
                           "source": "book.png"
                       }
                   },
                   "left": {
                       "image": {
                           "source": "line.png",
                           "region": [0, 0, 6, 4],
                           "frame": [2, 4, 4, 0],
                           "padding": [0, 0, 0, 6]
                       }
                   },
                   "center": {
                       "image": {
                           "source": "line.png",
                           "region": [2, 0, 4, 4],
                           "frame": [0, 4, 4, 0],
                           "padding": [0, 0, 0, 6]
                       }
                   }
               },
               "frame": {
                   "image": {
                       "source": "panel.png",
                       "frame": [8, 8, 16, 16],
                       "padding": [16, 16, 8, 8]
                   }
               }
               }, resources_path='../theme/')

content = Frame(
    Scrollable(
        VerticalContainer([SectionHeader("Folding"),
                        Document("Click on the section headers below to open them.", width=300),
                        FoldingSection("Folding 1", Document("This is the first folding.", width=300)),
                        FoldingSection("Folding 2", Document("This is the second folding.", width=300),
                                       is_open=False),
                        FoldingSection("Folding 3", Document("This is the third folding.", width=300),
                                       is_open=False),
                        ], align=HALIGN_LEFT),
        height=400)
)

Manager(
    content
    ,
    window=window, batch=batch,
    anchor=ANCHOR_CENTER,
    theme=theme)

pyglet.app.run()
