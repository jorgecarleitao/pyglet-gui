import unittest
import os
import sys

import pyglet
import pyglet_gui.theme


class TestPygletGUI(unittest.TestCase):
    """
    Default configuration of testing unit.
    """
    def setUp(self):
        # define a theme
        self.theme = pyglet_gui.theme.ThemeFromPath(os.path.join(sys.path[0], '../theme'))

        self.window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
        self.batch = pyglet.graphics.Batch()

        @self.window.event
        def on_draw():
            self.window.clear()
            self.batch.draw()

    def tearDown(self):
        self.window.close()
