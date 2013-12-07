import os
import sys
sys.path.insert(0, os.path.abspath('../'))

import pyglet


window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
batch = pyglet.graphics.Batch()
bg_group = pyglet.graphics.OrderedGroup(0)
fg_group = pyglet.graphics.OrderedGroup(1)
fps = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps.draw()

# register event to update pyglet-gui
window.register_event_type('on_update')


def update(dt):
    window.dispatch_event('on_update', dt)
pyglet.clock.schedule(update)
