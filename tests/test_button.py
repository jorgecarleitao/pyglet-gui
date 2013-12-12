from .setup import TestPygletGUI

from pyglet_gui.dialog import Dialog
from pyglet_gui.buttons import Button


class TestButton(TestPygletGUI):

    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = Button(label="test")
        self.dialog = Dialog(self.button, window=self.window, batch=self.batch, theme=self.theme)

    def test_creation(self):
        self.assertNotEqual(self.button.width, 0)
        self.assertNotEqual(self.button.height, 0)
        self.assertNotEqual(self.button._label, None)
        self.assertNotEqual(self.button._button, None)

    def test_press(self):
        self.button.on_mouse_press(0, 0, None, None)
        self.assertEqual(self.button.is_pressed(), True)

    def test_delete(self):
        self.dialog.delete()

        self.assertEqual(self.button._button, None)
        self.assertEqual(self.button._label, None)
