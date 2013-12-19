from .setup import TestPygletGUI

from pyglet_gui.core import Viewer
from pyglet_gui.dialog import Dialog

import pyglet_gui.constants


class TestDialog(TestPygletGUI):
    """
    This test case tests basic functionality of
    widget+dialog. We use an empty widget for this.
    """

    def setUp(self):
        super().setUp()

        self.widget = Viewer(width=50, height=50)
        self.dialog = Dialog(self.widget, window=self.window, batch=self.batch, theme=self.theme)

    def test_top_down_draw(self):
        """
        Tests that the dialog's size was set
        according to the child size.
        """
        # dialog size is correct
        self.assertEqual(self.dialog.width, 50)
        self.assertEqual(self.dialog.height, 50)

        # widget is centered in the window
        self.assertEqual(self.widget.x, self.window.width/2 - self.widget.width/2)
        self.assertEqual(self.widget.y, self.window.height/2 - self.widget.height/2)

    def test_bottom_up_draw(self):
        """
        Tests that the dialog's size is modified
        if we set a new size to the widget.
        """
        self.widget.width = 60
        self.widget.parent.reset_size()

        # dialog size was reset
        self.assertEqual(self.dialog.width, self.widget.width)

        # widget and dialog were re-centered in the window
        self.assertEqual(self.widget.x, self.window.width/2 - self.widget.width/2)
        self.assertEqual(self.dialog.x, self.window.width/2 - self.dialog.width/2)

    def test_substitute_widget(self):
        """
        Tests substitution of dialog's content
        by other widget.
        """
        self.new_widget = Viewer(width=60, height=50)

        self.dialog.content = self.new_widget

        self.assertTrue(not self.widget.has_manager())
        self.assertFalse(self.widget.is_loaded)

        self.assertTrue(self.new_widget.has_manager())
        self.assertTrue(self.new_widget.is_loaded)

        # dialog size was reset, new widget position is correct
        self.assertEqual(self.dialog.width, self.new_widget.width)
        self.assertEqual(self.new_widget.x, self.window.width/2 - self.new_widget.width/2)

    def test_window_resize(self):
        self.window.width = 100
        self.dialog.on_resize(self.window.width, self.window.height)

        # dialog size didn't changed.
        self.assertEqual(self.dialog.width, 50)

        # dialog is still centered.
        self.assertEqual(self.dialog.x, self.window.width/2 - self.dialog.width/2)

    def test_change_offset(self):
        self.dialog.offset = (10, 0)

        # dialog is centered with an offset.
        self.assertEqual(self.dialog.x - 10, self.window.width/2 - self.dialog.width/2)

    def test_change_anchor(self):
        self.dialog.anchor = pyglet_gui.constants.ANCHOR_TOP_LEFT

        # dialog is in correct position.
        self.assertEqual(self.dialog.x, 0)

    def test_new_dialog_is_on_top(self):
        other_dialog = Dialog(Viewer(width=50, height=50), window=self.window,
                              batch=self.batch,
                              theme=self.theme)

        # confirm that a new dialog starts always on top
        self.assertTrue(other_dialog.root_group.is_on_top())

    def test_new_dialog_without_window(self):
        other_dialog = Dialog(Viewer(width=50, height=50),
                              batch=self.batch,
                              theme=self.theme)

        # confirm that a new dialog without window starts
        # with no size
        self.assertTrue(other_dialog.width, 0)

        # change the dialog's window
        other_dialog.window = self.window

        # confirm it has a size.
        self.assertEqual(self.dialog.width, 50)

        # confirm it is in the correct position
        self.assertEqual(self.dialog.x, self.window.width/2 - self.dialog.width/2)

    def test_deletion(self):
        self.dialog.delete()

        # confirm that widget is also deleted
        self.assertTrue(not self.widget.has_manager())

    def tearDown(self):
        self.dialog.delete()
        super().tearDown()

if __name__ == "__main__":
    import unittest
    unittest.main()
