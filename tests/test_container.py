from .setup import TestPygletGUI

from pyglet_gui.widgets import Widget
from pyglet_gui.dialog import Dialog
from pyglet_gui.containers import Container


class TestContainer(TestPygletGUI):
    """
    This test case tests basic functionality of
    a container. We use an empty widgets for this.
    """

    def setUp(self):
        super().setUp()

        self.container = Container([Widget(width=50, height=50),
                                    Widget(width=50, height=50)])

        self.dialog = Dialog(self.container, window=self.window, batch=self.batch, theme=self.theme)

    def test_set_manager(self):
        """
        Tests that the manager is set for every children.
        """
        # dialog size is correct
        for item in self.container.content:
            self.assertTrue(item.has_manager())

    def test_deletion(self):
        self.dialog.delete()

        # confirm that widget is also deleted
        for item in self.container.content:
            self.assertFalse(item.has_manager())

    def tearDown(self):
        self.dialog.delete()
        super().tearDown()

if __name__ == "__main__":
    import unittest
    unittest.main()
