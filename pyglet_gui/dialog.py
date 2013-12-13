import pyglet
from pyglet import gl

from pyglet_gui.core import Manager, Managed, Controller
from pyglet_gui.widgets import Rectangle
from pyglet_gui.constants import GetRelativePoint, ANCHOR_CENTER
from pyglet_gui.containers import Wrapper


next_dialog_order_id = 0


def GetNextDialogOrderId():
    global next_dialog_order_id
    next_dialog_order_id += 1
    return next_dialog_order_id


class DialogGroup(pyglet.graphics.OrderedGroup):
    """
    Ensure that all Widgets within a Dialog can be drawn with
    blending enabled, and that our Dialog will be drawn in a particular
    order relative to other Dialogs.
    """
    def __init__(self, parent=None):
        """
        Creates a new DialogGroup.  By default we'll be on top.

        @param parent Parent group
        """
        pyglet.graphics.OrderedGroup.__init__(self, GetNextDialogOrderId(), parent)
        self.own_order = self.order

    def __eq__(self, other):
        """
        When compared with other DialogGroups, we'll return our real order
        compared against theirs; otherwise use the OrderedGroup comparison.
        """
        if isinstance(other, DialogGroup):
            return self.own_order == other.own_order
        else:
            return pyglet.graphics.OrderedGroup.__eq__(self, other)

    def __lt__(self, other):
        if isinstance(other, DialogGroup):
            return self.own_order < other.own_order
        else:
            return pyglet.graphics.OrderedGroup.__lt__(self, other)

    def __hash__(self):
        return hash((self.order, self.parent))

    def is_on_top(self):
        """
        Are we the top dialog group?
        """
        global next_dialog_order_id
        return self.own_order == next_dialog_order_id

    def pop_to_top(self):
        """
        Put us on top of other dialog groups.
        """
        self.own_order = GetNextDialogOrderId()

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


class Dialog(Wrapper, Manager):
    def __init__(self, content=None, window=None, batch=None, group=None,
                 anchor=ANCHOR_CENTER, offset=(0, 0),
                 theme=None, movable=True):
        assert isinstance(theme, dict)
        Wrapper.__init__(self, content=content)
        Manager.__init__(self)

        self.window = window
        self.anchor = anchor
        self.offset = offset
        self._theme = theme
        self._manager = self
        self.is_movable = movable
        if batch is None:
            self.batch = pyglet.graphics.Batch()
            self._has_own_batch = True
        else:
            self.batch = batch
            self._has_own_batch = False
        self.root_group = DialogGroup(parent=group)
        self.group = {'panel': pyglet.graphics.OrderedGroup(10, self.root_group),
                      'background': pyglet.graphics.OrderedGroup(20, self.root_group),
                      'foreground': pyglet.graphics.OrderedGroup(30, self.root_group),
                      'highlight': pyglet.graphics.OrderedGroup(40, self.root_group)}

        self._is_dragging = False

        if window is None:
            self.screen = Rectangle()
        else:
            width, height = window.get_size()
            self.screen = Rectangle(width=width, height=height)
            window.push_handlers(self)

        content.set_manager(self)
        self.load()
        self.reset_size(reset_parent=False)
        self.set_position(*self.get_position())

    @Managed.theme.getter
    def theme(self):
        return self._theme

    def get_position(self):
        # Calculate our position relative to our containing window,
        # making sure that we fit completely on the window.  If our offset
        # would send us off the screen, constrain it.
        x, y = GetRelativePoint(self.screen, self.anchor, self, None, (0, 0))
        max_offset_x = self.screen.width - self.width - x
        max_offset_y = self.screen.height - self.height - y
        offset_x, offset_y = self.offset
        offset_x = max(min(offset_x, max_offset_x), -x)
        offset_y = max(min(offset_y, max_offset_y), -y)
        self.offset = (offset_x, offset_y)
        x += offset_x
        y += offset_y

        return x, y

    def reset_size(self, reset_parent=True):
        # Dialog never has parent and thus never reset_parent.
        super().reset_size(reset_parent=False)
        self.set_position(*self.get_position())

    def draw(self):
        assert self._has_own_batch
        self.batch.draw()

    def get_root(self):
        return self

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not Manager.on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
            if self.is_movable and self._is_dragging:
                x, y = self.offset
                self.offset = (int(x + dx), int(y + dy))
                self.set_position(*self.get_position())
                return pyglet.event.EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        """
        This puts the dialog always on top, both batch and event stack.
        """
        Manager.on_mouse_motion(self, x, y, dx, dy)
        if self.hit_test(x, y):
            if not self.root_group.is_on_top():
                self.pop_to_top()
            return pyglet.event.EVENT_HANDLED

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
        retval = Manager.on_mouse_press(self, x, y, button, modifiers)
        if self.hit_test(x, y):
            if not retval:
                self._is_dragging = True
                retval = pyglet.event.EVENT_HANDLED
        return retval

    def on_mouse_release(self, x, y, button, modifiers):
        self._is_dragging = False
        return Manager.on_mouse_release(self, x, y, button, modifiers)

    def on_resize(self, width, height):
        """
        Update our knowledge of the window's width and height.
        """
        if self.screen.width != width or self.screen.height != height:
            self.screen.width, self.screen.height = width, height
            self.set_position(*self.get_position())

    def pop_to_top(self):
        """
        Pop our dialog group to the top, and force our batch to re-sort
        the groups. Also, puts our event handler on top of the window's
        event handler stack.
        """
        self.root_group.pop_to_top()
        self.batch._draw_list_dirty = True  # forces resorting groups
        if self.window is not None:
            self.window.remove_handlers(self)
            self.window.push_handlers(self)

    def delete(self):
        Wrapper.delete(self)
        if self.window is not None:
            self.window.remove_handlers(self)
            self.window = None
        Manager.delete(self)
        self.batch._draw_list_dirty = True  # forces resorting groups

events = ['on_key_press',
          'on_key_release',

          'on_text',
          'on_text_motion',
          'on_text_motion_select',

          'on_mouse_motion',
          'on_mouse_drag',
          'on_mouse_press',
          'on_mouse_release',
          'on_mouse_scroll',

          'on_resize']

for event_type in events:
    Dialog.register_event_type(event_type)
