from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import Frame, VerticalLayout
from pyglet_gui.document import Document
from pyglet_gui.constants import ANCHOR_CENTER, HALIGN_LEFT
from pyglet_gui.gui import SectionHeader, FoldingSection
from pyglet_gui.scrollable import Scrollable

document0 = pyglet.text.decode_attributed("""
Click on the section headers below to open them.
""")

document1 = pyglet.text.decode_attributed("""
This is the first folding.
""")
document2 = pyglet.text.decode_attributed("""
This is the second folding.
""")
document3 = pyglet.text.decode_attributed("""
This is the third folding.
""")

content = Frame(
    Scrollable(
        VerticalLayout([SectionHeader("Folding"),
                        Document(document0, width=300),
                        FoldingSection("Folding 1", Document(document1, width=300)),
                        FoldingSection("Folding 2", Document(document2, width=300), is_open=False),
                        FoldingSection("Folding 3", Document(document3, width=300), is_open=False),
                        ], align=HALIGN_LEFT),
        height=400)
)

Dialog(
    content
    ,
    window=window, batch=batch, group=fg_group,
    anchor=ANCHOR_CENTER,
    theme=theme)

pyglet.app.run()
