import os
import sys
sys.path.insert(0, os.path.abspath('../'))

import pyglet

window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    window.clear()
    batch.draw()
