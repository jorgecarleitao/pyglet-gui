from .setup import TestPygletGUI

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button


class TestButton(TestPygletGUI):

    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = Button(label="test")
        self.manager = Manager(self.button, window=self.window, batch=self.batch, theme=self.theme)

    def test_creation(self):
        self.assertNotEqual(self.button.width, 0)
        self.assertNotEqual(self.button.height, 0)
        self.assertEqual(self.button.is_loaded, True)

    def test_press(self):
        self.button.on_mouse_press(0, 0, None, None)
        self.assertEqual(self.button.is_pressed, True)

    def test_delete(self):
        self.manager.delete()

        self.assertEqual(self.button.is_loaded, False)

if __name__ == "__main__":
    import unittest
    unittest.main()
