from pyglet_gui.constants import ANCHOR_CENTER
from pyglet_gui.manager import ViewerManager, ControllerManager


class Dialog(ViewerManager, ControllerManager):
    def __init__(self,
                 content,
                 theme,
                 window=None,
                 batch=None,
                 group=None,
                 is_movable=True,
                 anchor=ANCHOR_CENTER,
                 offset=(0, 0)):
        ControllerManager.__init__(self)
        ViewerManager.__init__(self, content, theme, window, batch, group, anchor, offset)

        self.is_movable = is_movable
        self._is_dragging = False

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not ControllerManager.on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
            if self.is_movable and self._is_dragging:
                x, y = self._offset
                self._offset = (int(x + dx), int(y + dy))
                self.set_position(*self.get_position())
                return True

    def on_mouse_motion(self, x, y, dx, dy):
        ControllerManager.on_mouse_motion(self, x, y, dx, dy)
        if self.hit_test(x, y):
            if not self.root_group.is_on_top():
                self.pop_to_top()
            return True

    def on_mouse_press(self, x, y, button, modifiers):
        """
        If the focus is set, and the target lies within the focus, pass the
        message down.  Otherwise, check if we need to assign a new focus.
        If the mouse was pressed within our frame but no control was targeted,
        we may be setting up to drag the Dialog around.

        @param x X coordinate of mouse
        @param y Y coordinate of mouse
        @param button Button pressed
        @param modifiers Modifiers to apply to button
        """
        retval = ControllerManager.on_mouse_press(self, x, y, button, modifiers)
        if self.hit_test(x, y):
            if not retval:
                self._is_dragging = True
                retval = True
        return retval

    def on_mouse_release(self, x, y, button, modifiers):
        self._is_dragging = False
        return ControllerManager.on_mouse_release(self, x, y, button, modifiers)

    def on_resize(self, width, height):
        """
        Update our knowledge of the window's width and height.
        """
        if self.screen.width != width or self.screen.height != height:
            self.screen.width, self.screen.height = width, height
            self.set_position(*self.get_position())

    def delete(self):
        ViewerManager.delete(self)
        ControllerManager.delete(self)
