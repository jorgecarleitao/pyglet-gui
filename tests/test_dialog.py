from .setup import TestPygletGUI

from pyglet_gui.manager import Manager
from pyglet_gui.core import Viewer

import pyglet_gui.constants


class TestDialog(TestPygletGUI):
    """
    This test case tests basic functionality of
    widget+manager. We use an empty widget for this.
    """

    def setUp(self):
        super(TestDialog, self).setUp()

        self.widget = Viewer(width=50, height=50)
        self.manager = Manager(self.widget, window=self.window, batch=self.batch, theme=self.theme)

    def test_top_down_draw(self):
        """
        Tests that the manager's size was set
        according to the child size.
        """
        # manager size is correct
        self.assertEqual(self.manager.width, 50)
        self.assertEqual(self.manager.height, 50)

        # widget is centered in the window
        self.assertEqual(self.widget.x, self.window.width/2 - self.widget.width/2)
        self.assertEqual(self.widget.y, self.window.height/2 - self.widget.height/2)

    def test_bottom_up_draw(self):
        """
        Tests that the manager's size is modified
        if we set a new size to the widget.
        """
        self.widget.width = 60
        self.widget.parent.reset_size()

        # manager size was reset
        self.assertEqual(self.manager.width, self.widget.width)

        # widget and manager were re-centered in the window
        self.assertEqual(self.widget.x, self.window.width/2 - self.widget.width/2)
        self.assertEqual(self.manager.x, self.window.width/2 - self.manager.width/2)

    def test_substitute_widget(self):
        """
        Tests substitution of manager's content
        by other widget.
        """
        self.new_widget = Viewer(width=60, height=50)

        self.manager.content = self.new_widget

        self.assertTrue(not self.widget.has_manager())
        self.assertFalse(self.widget.is_loaded)

        self.assertTrue(self.new_widget.has_manager())
        self.assertTrue(self.new_widget.is_loaded)

        # manager size was reset, new widget position is correct
        self.assertEqual(self.manager.width, self.new_widget.width)
        self.assertEqual(self.new_widget.x, self.window.width/2 - self.new_widget.width/2)

    def test_window_resize(self):
        self.window.width = 100
        self.manager.on_resize(self.window.width, self.window.height)

        # manager size didn't changed.
        self.assertEqual(self.manager.width, 50)

        # manager is still centered.
        self.assertEqual(self.manager.x, self.window.width/2 - self.manager.width/2)

    def test_change_offset(self):
        self.manager.offset = (10, 0)

        # manager is centered with an offset.
        self.assertEqual(self.manager.x - 10, self.window.width/2 - self.manager.width/2)

    def test_change_anchor(self):
        self.manager.anchor = pyglet_gui.constants.ANCHOR_TOP_LEFT

        # manager is in correct position.
        self.assertEqual(self.manager.x, 0)

    def test_new_manager_is_on_top(self):
        other_manager = Manager(Viewer(width=50, height=50), window=self.window,
                              batch=self.batch,
                              theme=self.theme)

        # confirm that a new manager starts always on top
        self.assertTrue(other_manager.root_group.is_on_top())

    def test_new_manager_without_window(self):
        other_manager = Manager(Viewer(width=50, height=50),
                              batch=self.batch,
                              theme=self.theme)

        # confirm that a new manager without window starts
        # with no size
        self.assertTrue(other_manager.width, 0)

        # change the manager's window
        other_manager.window = self.window

        # confirm it has a size.
        self.assertEqual(self.manager.width, 50)

        # confirm it is in the correct position
        self.assertEqual(self.manager.x, self.window.width/2 - self.manager.width/2)

    def test_deletion(self):
        self.manager.delete()

        # confirm that widget is also deleted
        self.assertTrue(not self.widget.has_manager())

    def tearDown(self):
        self.manager.delete()
        super(TestDialog, self).tearDown()

if __name__ == "__main__":
    import unittest
    unittest.main()
