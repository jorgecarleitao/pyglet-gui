from .setup import TestPygletGUI

from pyglet_gui.widgets import Widget
from pyglet_gui.dialog import Dialog


class TestViewer(TestPygletGUI):
    """
    This test case tests basic functionality of
    viewer+dialog. We use an empty widget for this.
    """

    def setUp(self):
        super().setUp()

        self.widget = Widget(width=50, height=50)
        self.dialog = Dialog(self.widget, window=self.window, batch=self.batch, theme=self.theme)

    def test_top_down(self):
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

    def test_bottom_up(self):
        """
        Tests that the dialog's size is modified
        if we set a new size to the widget.
        """
        self.widget.width = 60
        self.widget.parent.reset_size()
        self.assertEqual(self.dialog.width, self.widget.width)

        # widget and dialog are re-centered in the window
        self.assertEqual(self.widget.x, self.window.width/2 - self.widget.width/2)
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
