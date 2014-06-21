from .setup import TestPygletGUI

import pyglet.window
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, FocusButton


class GenericButtonTest(object):
    def setUp(self):
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


class TestButton(TestPygletGUI, GenericButtonTest):
    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = Button(label="test")
        GenericButtonTest.setUp(self)


class TestOneTimeButton(TestPygletGUI, GenericButtonTest):
    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = OneTimeButton(label="test")
        GenericButtonTest.setUp(self)


class TestCheckbox(TestPygletGUI, GenericButtonTest):
    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = Checkbox(label="test")
        GenericButtonTest.setUp(self)

    def test_get_path(self):
        self.assertEqual(self.button.get_path(), ['checkbox', 'unchecked'])
        self.button.on_mouse_press(0, 0, None, None)
        self.assertEqual(self.button.get_path(), ['checkbox', 'checked'])


class TestFocusButton(TestPygletGUI, GenericButtonTest):
    def setUp(self):
        TestPygletGUI.setUp(self)
        self.button = FocusButton(label="test")
        GenericButtonTest.setUp(self)

    def test_key_press(self):
        self.assertEqual(self.button.is_pressed, False)
        self.button.on_key_press(pyglet.window.key.ENTER,None)
        self.assertEqual(self.button.is_pressed, True)


if __name__ == "__main__":
    import unittest
    unittest.main()
