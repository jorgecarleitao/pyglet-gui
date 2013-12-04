from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.buttons import Button
from pyglet_gui.containers import VerticalLayout, HorizontalLayout, GridLayout

# Set up a Dialog

hlay = HorizontalLayout(content=[VerticalLayout(content=[Button("(1,1)"), Button("(1,2)")]),
                                 VerticalLayout(content=[Button("(2,1)"), Button("(2,2)")])])

grid = GridLayout([[Button("(1,1)"), Button("(1,2)")],
                   [Button("(2,1)"), Button("(2,2)")]])

vlay = VerticalLayout([hlay, grid])

dialog = Dialog(vlay, window=window, batch=batch, theme=theme)

pyglet.app.run()
