from .setup import TestPygletGUI

from pyglet_gui.core import Viewer
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import VerticalLayout


class TestVerticalContainer(TestPygletGUI):
    """
    This test case tests basic functionality of
    a vertical container.
    """

    def setUp(self):
        super().setUp()

        self.container = VerticalLayout([Viewer(width=50, height=50),
                                         Viewer(width=50, height=50)])

        self.dialog = Dialog(self.container, window=self.window, batch=self.batch, theme=self.theme)

    def _test_content_position(self):
        """
        Tests the position of the two widgets within the container.
        """
        # first widget y is the top y (container.y + container.height) minus its size (container.content[0].height)
        self.assertEqual(self.container.content[0].y,
                         self.container.y + self.container.height - self.container.content[0].height)

        # second widget y is the top y (container.y + container.height - container.content[0].height) minus its size
        # (container.content[1].height) minus the padding (self.container.padding)
        self.assertEqual(self.container.content[1].y,
                         self.container.y + self.container.height
                         - self.container.content[0].height - self.container.content[1].height
                         - self.container.padding)

    def test_top_down_draw(self):
        """
        Tests that the container's size was set correctly
        and the positions of its content is correct.
        """
        # dialog size is correct
        self.assertEqual(self.container.width, 50)
        self.assertEqual(self.container.height, 100 + self.container.padding)

        # widget is centered in the window
        self.assertEqual(self.container.x, self.window.width / 2 - self.container.width / 2)
        self.assertEqual(self.container.y, self.window.height / 2 - self.container.height / 2)

        self._test_content_position()

    def test_bottom_up_draw(self):
        """
        Tests that the dialog's size is modified
        if we set a new size to the widget.
        """
        self.container.content[0].width = 60
        self.container.content[0].height = 60
        self.container.content[0].parent.reset_size()

        # container width was set
        self.assertEqual(self.container.width, 60)
        # container height was set
        self.assertEqual(self.container.height, 110 + self.container.padding)

        # container was re-centered in the window
        self.assertEqual(self.container.x, self.window.width / 2 - self.container.width / 2)
        self.assertEqual(self.container.y, self.window.height / 2 - self.container.height / 2)

        self._test_content_position()

    def test_add_widget(self):
        self.container.add(Viewer(width=50, height=50))

        self.assertEqual(self.dialog.width, 50)
        self.assertEqual(self.dialog.height, 150 + 2 * self.container.padding)

        self._test_content_position()

    def test_remove_widget(self):
        self.container.remove(self.container.content[0])

        self.assertEqual(self.dialog.width, 50)
        self.assertEqual(self.dialog.height, 50 + self.container.padding)

    def tearDown(self):
        self.dialog.delete()
        super().tearDown()


if __name__ == "__main__":
    import unittest

    unittest.main()
