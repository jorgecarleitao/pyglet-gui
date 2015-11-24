import pyglet
from pyglet import gl

from pyglet_gui.constants import ANCHOR_CENTER, GetRelativePoint
from pyglet_gui.core import Rectangle
from pyglet_gui.containers import Wrapper


class ViewerManagerGroup(pyglet.graphics.OrderedGroup):
    """
    Ensure that Viewers inside Manager can be drawn with
    blending enabled, and that Managers are drawn in a particular
    order.
    """
    _top_manager_order = 0

    @classmethod
    def _get_next_top_order(cls):
        cls._top_manager_order += 1
        return cls._top_manager_order

    def __init__(self, parent=None):
        """
        Creates a new ViewerManagerGroup. By default it is on top.
        """
        pyglet.graphics.OrderedGroup.__init__(self, self._get_next_top_order(), parent)
        self.own_order = self.order

    def __eq__(self, other):
        """
        When compared with other ViewerManagerGroups, we'll return the own_order
        compared against theirs; otherwise use the OrderedGroup comparison.
        """
        if isinstance(other, ViewerManagerGroup):
            return self.own_order == other.own_order
        else:
            return pyglet.graphics.OrderedGroup.__eq__(self, other)

    def __lt__(self, other):
        if isinstance(other, ViewerManagerGroup):
            return self.own_order < other.own_order
        else:
            return pyglet.graphics.OrderedGroup.__lt__(self, other)

    def __hash__(self):
        return hash((self.order, self.parent))

    def is_on_top(self):
        """
        Are we the top manager group?
        """
        return self.own_order == self._top_manager_order

    def pop_to_top(self):
        """
        Put us on top of other manager groups.
        """
        self.own_order = self._get_next_top_order()

    def set_state(self):
        """
        Ensure that blending is set.
        """
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_CURRENT_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        """
        Restore previous blending state.
        """
        gl.glPopAttrib()


class ViewerManager(Wrapper):
    def __init__(self, content,
                 theme,
                 window=None,
                 batch=None,
                 group=None,
                 anchor=ANCHOR_CENTER,
                 offset=(0, 0)):
        super(ViewerManager, self).__init__(content, anchor=anchor)

        assert isinstance(theme, dict)
        self._theme = theme
        self._manager = self
        self._offset = offset

        if batch is None:
            self._batch = pyglet.graphics.Batch()
            self._has_own_batch = True
        else:
            self._batch = batch
            self._has_own_batch = False

        self._root_group = ViewerManagerGroup(parent=group)
        self.group = {'panel': pyglet.graphics.OrderedGroup(10, self.root_group),
                      'background': pyglet.graphics.OrderedGroup(20, self.root_group),
                      'foreground': pyglet.graphics.OrderedGroup(30, self.root_group),
                      'highlight': pyglet.graphics.OrderedGroup(40, self.root_group)}

        self.content.set_manager(self)
        self.content.parent = self

        self.screen = Rectangle()
        self.load()

        self._window = None
        self.window = window

    @property
    def root_group(self):
        return self._root_group

    @property
    def batch(self):
        return self._batch

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        if self._window is not None:
            self._window.remove_handlers(self)
        self._window = window

        if self._window is None:
            self.unload()
            self.screen = Rectangle()
        else:
            width, height = window.get_size()
            self.screen = Rectangle(width=width, height=height)
            window.push_handlers(self)

        # make a top-down reset_size.
        self.reset_size(reset_parent=False)

        # and set the new position.
        self.set_position(*self.get_position())

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        assert isinstance(offset, tuple)
        assert len(offset) == 2
        self._offset = offset
        self.set_position(*self.get_position())

    @Wrapper.theme.getter
    def theme(self):
        return self._theme

    @Wrapper.anchor.setter
    def anchor(self, anchor):
        self._anchor = anchor
        self.set_position(*self.get_position())

    def get_position(self):
        # Calculate our position relative to our containing window,
        # making sure that we fit completely on the window.  If our offset
        # would send us off the screen, constrain it.
        x, y = GetRelativePoint(self.screen, self.anchor, self, None, (0, 0))
        max_offset_x = self.screen.width - self.width - x
        max_offset_y = self.screen.height - self.height - y
        offset_x, offset_y = self._offset
        offset_x = max(min(offset_x, max_offset_x), -x)
        offset_y = max(min(offset_y, max_offset_y), -y)
        self._offset = (offset_x, offset_y)
        x += offset_x
        y += offset_y

        return x, y

    def reset_size(self, reset_parent=True):
        # Manager never has parent and thus never reset_parent.
        super(ViewerManager, self).reset_size(reset_parent=False)

        # if is a bottom-up, we have to reposition ourselves.
        if reset_parent:
            self.set_position(*self.get_position())

    def draw(self):
        assert self._has_own_batch
        self._batch.draw()

    def pop_to_top(self):
        """
        Puts the manager on top of the other dialogs on the same batch (and window).
        - Pops the manager group to the top
        - Puts the event handler on top of the event handler's stack of the window.
        """
        self._root_group.pop_to_top()
        self._batch._draw_list_dirty = True  # forces resorting groups
        if self._window is not None:
            self._window.remove_handlers(self)
            self._window.push_handlers(self)

    def delete(self):
        Wrapper.delete(self)
        if self._window is not None:
            self._window.remove_handlers(self)
            self._window = None
        self._batch._draw_list_dirty = True  # forces resorting groups


class ControllerManager:
    def __init__(self):
        self._controllers = []  # list of controllers.

        self._hover = None  # the control that is being hovered (mouse inside)
        self._focus = None  # the control that has the focus (accepts key strokes)

        self.wheel_target = None  # the primary control to receive wheel events.
        self.wheel_hint = None    # the secondary control to receive wheel events.

    @property
    def controllers(self):
        return self._controllers

    def add_controller(self, controller):
        assert controller not in self._controllers
        self._controllers.append(controller)

    def remove_controller(self, controller):
        assert controller in self._controllers
        self._controllers.remove(controller)
        if self._hover == controller:
            self.set_hover(None)
        if self._focus == controller:
            self.set_focus(None)

    def set_next_focus(self, direction):
        assert direction in [-1, 1]

        # all the focusable controllers
        focusable = [x for x in self._controllers if hasattr(x, 'on_gain_focus')]
        if not focusable:
            return

        if self._focus is not None and self._focus in focusable:
            index = focusable.index(self._focus)
        else:
            index = 0 - direction

        new_focus = focusable[(index + direction) % len(focusable)]
        self.set_focus(new_focus)

    def on_key_press(self, symbol, modifiers):
        ## move between focusable controllers.
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                direction = -1
            else:
                direction = 1

            self.set_next_focus(direction)
            return True  # we only change focus on the manager we are in.

        if self._focus is not None and hasattr(self._focus, 'on_key_press'):
            return self._focus.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self._focus is not None and hasattr(self._focus, 'on_key_release'):
            return self._focus.on_key_release(symbol, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._focus is not None and hasattr(self._focus, 'on_mouse_drag'):
            return self._focus.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        new_hover = None
        for control in self._controllers:
            if control.hit_test(x, y):
                new_hover = control
                break
        self.set_hover(new_hover)

        if self._hover is not None and hasattr(self._hover, 'on_mouse_motion'):
            return self._hover.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_focus(self._hover)
        if self._focus and hasattr(self._focus, 'on_mouse_press'):
            return self._focus.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self._focus is not None and hasattr(self._focus, 'on_mouse_release'):
            return self._focus.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.wheel_target in self._controllers:
            return self.wheel_target.on_mouse_scroll(x, y, scroll_x, scroll_y)
        elif self.wheel_hint in self._controllers:
            return self.wheel_hint.on_mouse_scroll(x, y, scroll_x, scroll_y)
        else:
            return False

    def on_text(self, text):
        if self._focus and text != '\r' and hasattr(self._focus, 'on_text'):
            return self._focus.on_text(text)

    def on_text_motion(self, motion):
        if self._focus and hasattr(self._focus, 'on_text_motion'):
            return self._focus.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._focus and hasattr(self._focus, 'on_text_motion_select'):
            return self._focus.on_text_motion_select(motion)

    def set_focus(self, focus):
        if self._focus == focus:
            return
        if self._focus is not None and hasattr(self._focus, 'on_lose_focus'):
            self._focus.on_lose_focus()
        self._focus = focus
        if focus is not None and hasattr(self._focus, 'on_gain_focus'):
            self._focus.on_gain_focus()

    def set_hover(self, hover):
        if self._hover == hover:
            return
        if self._hover is not None and hasattr(self._hover, 'on_lose_highlight'):
            self._hover.on_lose_highlight()
        self._hover = hover
        if hover is not None and hasattr(self._hover, 'on_gain_highlight'):
            hover.on_gain_highlight()

    def set_wheel_hint(self, control):
        self.wheel_hint = control

    def set_wheel_target(self, control):
        self.wheel_target = control

    def delete(self):
        self._controllers = []
        self._focus = None
        self._hover = None
        self.wheel_hint = None
        self.wheel_target = None


class Manager(ViewerManager, ControllerManager):
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
            if not self._root_group.is_on_top():
                self.pop_to_top()
            return True

    def on_mouse_press(self, x, y, button, modifiers):
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
