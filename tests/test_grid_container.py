from .setup import TestPygletGUI

from pyglet_gui.widgets import Widget
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import GridLayout


class TestGridContainer(TestPygletGUI):
    """
    This test case tests basic functionality of
    a grid container.
    """

    def setUp(self):
        super().setUp()

        self.container = GridLayout([[Widget(width=50, height=50), Widget(width=50, height=50)],
                                     [Widget(width=50, height=50), Widget(width=50, height=50)]])

        self.dialog = Dialog(self.container, window=self.window, batch=self.batch, theme=self.theme)

    def test_top_down_draw(self):
        """
        Tests that the container's size was set correctly
        and the positions of its content is correct.
        """
        # dialog size is correct
        self.assertEqual(self.container.width, 100 + self.container.padding)
        self.assertEqual(self.container.height, 100 + self.container.padding)

        # widget is centered in the window
        self.assertEqual(self.container.x, self.window.width / 2 - self.container.width / 2)
        self.assertEqual(self.container.y, self.window.height / 2 - self.container.height / 2)

    def test_bottom_up_draw(self):
        """
        Tests that the dialog's size is modified
        if we set a new size to the widget.
        """
        self.container.content[0][0].width = 60
        self.container.content[0][0].height = 60
        self.container.content[0][0].parent.reset_size()

        # container width was set
        self.assertEqual(self.container.width, 110 + self.container.padding)
        # container height was set
        self.assertEqual(self.container.height, 110 + self.container.padding)

        # container was re-centered in the window
        self.assertEqual(self.container.x, self.window.width / 2 - self.container.width / 2)
        self.assertEqual(self.container.y, self.window.height / 2 - self.container.height / 2)

    def test_add_row(self):
        self.container.add_row([Widget(width=50, height=50),
                                Widget(width=50, height=50),
                                Widget(width=50, height=50)])

        self.assertEqual(self.container.width, 150 + 2 * self.container.padding)
        self.assertEqual(self.container.height, 150 + 2 * self.container.padding)

    def test_add_column(self):
        self.container.add_column([Widget(width=50, height=50),
                                   Widget(width=50, height=50),
                                   Widget(width=50, height=50)])

        self.assertEqual(self.container.width, 150 + 2 * self.container.padding)
        self.assertEqual(self.container.height, 150 + 2 * self.container.padding)

    def test_substitute_element(self):
        self.container.set(1, 1, Widget(width=100, height=50))

        self.assertEqual(self.container.width, 150 + self.container.padding)
        self.assertEqual(self.container.height, 100 + self.container.padding)

    def tearDown(self):
        self.dialog.delete()
        super().tearDown()


if __name__ == "__main__":
    import unittest

    unittest.main()
