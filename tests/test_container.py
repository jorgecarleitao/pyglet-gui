from .setup import TestPygletGUI

from pyglet_gui.core import Viewer
from pyglet_gui.manager import Manager
from pyglet_gui.containers import Container


class TestContainer(TestPygletGUI):
    """
    This test case tests basic functionality of
    a container. We use an empty widgets for this.
    """

    def setUp(self):
        super().setUp()

        self.container = Container([Viewer(width=50, height=50),
                                    Viewer(width=50, height=50)])

        self.manager = Manager(self.container, window=self.window, batch=self.batch, theme=self.theme)

    def test_set_manager(self):
        """
        Tests that the manager is set for every children.
        """
        # manager size is correct
        for item in self.container.content:
            self.assertTrue(item.has_manager())

    def test_deletion(self):
        self.manager.delete()

        # confirm that widget is also deleted
        for item in self.container.content:
            self.assertFalse(item.has_manager())

    def test_add(self):
        """
        Tests that we can add a new item.
        """
        item = Viewer(width=50, height=50)
        self.container.add(item)

        self.assertEqual(item.has_manager(), True)

    def test_remove(self):
        """
        Tests that we can remove a new item.
        """
        item = self.container.content[0]
        self.container.remove(item)

        self.assertEqual(item.has_manager(), False)

    def tearDown(self):
        self.manager.delete()
        super().tearDown()

if __name__ == "__main__":
    import unittest
    unittest.main()
