import pyglet

from .setup import TestPygletGUI

from pyglet_gui.manager import Manager
from pyglet_gui.text_input import TextInput


class TestInput(TestPygletGUI):

    def setUp(self):
        TestPygletGUI.setUp(self)
        self.input = TextInput(text="test")
        self.manager = Manager(self.input, window=self.window, batch=self.batch, theme=self.theme)

    def test_focus(self):
        self.input.on_gain_focus()

        self.assertEqual(self.input.is_focus(), True)

        self.input.on_lose_focus()
        self.assertEqual(self.input.is_focus(), False)

    def test_input(self):
        self.assertEqual(self.input.get_text(), "test")
        self.input.on_gain_focus()
        self.input.on_text("text")
        self.assertEqual(self.input.get_text(), "text")  # it starts with all text selected, so 'test' is erased.
        self.input.on_text(" text")
        self.assertEqual(self.input.get_text(), "text text")

    def test_motion(self):
        self.input.on_gain_focus()

        self.input.on_text_motion(pyglet.window.key.MOTION_RIGHT)
        # 'test|' where | is the carret.
        self.assertEqual(self.input.get_text(), "test")

        self.input.on_text_motion(pyglet.window.key.MOTION_BACKSPACE)
        # 'tes|'
        self.assertEqual(self.input.get_text(), "tes")

        self.input.on_text_motion(pyglet.window.key.MOTION_LEFT)
        # 't|es'
        self.input.on_text_motion(pyglet.window.key.MOTION_LEFT)

        self.input.on_text_motion(pyglet.window.key.MOTION_DELETE)
        # 't|s'
        self.assertEqual(self.input.get_text(), "ts")
