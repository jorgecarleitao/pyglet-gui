from .setup import TestPygletGUI

import pyglet.window
from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton, Checkbox, FocusButton
from pyglet_gui.gui import PopupMessage


class TestPopupConfirm(TestPygletGUI):
    def setUp(self):
        TestPygletGUI.setUp(self)
        
        def callback(button):
            #set the flag on the test class so that it wont be deleted with the popup
            self.callback_done = True

        self.popup = PopupMessage(text="Test", window=self.window,
                                  batch=self.batch, theme=self.theme, on_escape=callback)

    def test_delete(self):
        self.popup.delete()
        self.assertEqual(self.popup.is_loaded, False)

    def test_on_click(self):
        button = self.popup.content.content.content[1]
        self.assertEqual(button.is_pressed, False)
        button.on_key_press(pyglet.window.key.ENTER, None)
        self.assertEqual(button.is_pressed, True)
        self.assertEqual(self.callback_done, True)

if __name__ == "__main__":
    import unittest
    unittest.main()
