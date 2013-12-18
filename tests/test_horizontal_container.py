from .setup import TestPygletGUI

from pyglet_gui.widgets import Widget
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import HorizontalLayout


class TestHorizontalContainer(TestPygletGUI):
    """
    This test case tests basic functionality of
    an horizontal container.
    """

    def setUp(self):
        super().setUp()

        self.container = HorizontalLayout([Widget(width=50, height=50),
                                           Widget(width=50, height=50)])

        self.dialog = Dialog(self.container, window=self.window, batch=self.batch, theme=self.theme)

    def _test_content_position(self):
        """
        Tests the position of the two widgets within the container.
        """
        # first widget x is the left x (container.x)
        self.assertEqual(self.container.content[0].x,
                         self.container.x)

        # second widget x is the left x (container.x + container.content[0].width)
        # plus the padding (self.container.padding)
        self.assertEqual(self.container.content[1].x,
                         self.container.x + self.container.content[0].width
                         + self.container.padding)

    def test_top_down_draw(self):
        """
        Tests that the dialog's size was set according to the child size.
        """
        # dialog size is correct
        self.assertEqual(self.dialog.width, 100 + self.container.padding)
        self.assertEqual(self.dialog.height, 50)

        # widget is centered in the window
        self.assertEqual(self.container.x, self.window.width/2 - self.container.width/2)
        self.assertEqual(self.container.y, self.window.height/2 - self.container.height/2)

        self._test_content_position()

    def test_bottom_up_draw(self):
        """
        Tests that the dialog's size is modified
        if we set a new size to the widget.
        """
        self.container.content[0].width = 60
        self.container.content[0].height = 60
        self.container.content[0].parent.reset_size()

        # dialog width was set
        self.assertEqual(self.dialog.width, 110 + self.container.padding)
        # container height was set
        self.assertEqual(self.container.height, 60)

        # container and dialog were re-centered in the window
        self.assertEqual(self.container.x, self.window.width/2 - self.container.width/2)
        self.assertEqual(self.dialog.y, self.window.height/2 - self.dialog.height/2)

        self._test_content_position()

    def test_add_widget(self):
        self.container.add(Widget(width=50, height=50))

        self.assertEqual(self.dialog.width, 150 + 2*self.container.padding)
        self.assertEqual(self.dialog.height, 50)

        self._test_content_position()

    def test_remove_widget(self):
        self.container.remove(self.container.content[0])

        self.assertEqual(self.dialog.width, 50 + self.container.padding)
        self.assertEqual(self.dialog.height, 50)

    def tearDown(self):
        self.dialog.delete()
        super().tearDown()

if __name__ == "__main__":
    import unittest
    unittest.main()
