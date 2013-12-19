import pyglet


class Managed():
    def __init__(self):
        self._manager = None

    def set_manager(self, manager):
        self._manager = manager

    def has_manager(self):
        return self._manager is not None

    def get_batch(self, group):
        return {'batch': self._manager.batch, 'group': self._manager.group[group]}

    @property
    def theme(self):
        assert self._manager is not None
        return self._manager.theme

    def delete(self):
        self._manager = None


class Rectangle():
    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self.width = width
        self.height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def is_inside(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


class Viewer(Rectangle, Managed):
    def __init__(self, width=0, height=0):
        super().__init__()
        self._parent = None
        self._is_loaded = False

        Rectangle.__init__(self, 0, 0, width, height)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, widget):
        self._parent = widget

    @property
    def is_loaded(self):
        return self._is_loaded

    def is_expandable(self):
        return False

    def set_position(self, x, y):
        super().set_position(x, y)
        self.layout()

    def get_path(self):
        raise NotImplementedError

    def load(self):
        assert not self._is_loaded
        self._is_loaded = True
        self.load_graphics()

    def unload(self):
        assert self._is_loaded
        self._is_loaded = False
        self.unload_graphics()

    def reload(self):
        self.unload()
        self.load()

    def load_graphics(self):
        pass

    def unload_graphics(self):
        pass

    def layout(self):
        pass

    def compute_size(self):
        return self.width, self.height

    def reset_size(self, reset_parent=True):
        width, height = self.compute_size()

        # we only reset the parent if we change size
        changed = False
        if self.width != width or self.height != height:
            self.width, self.height = width, height
            changed = True
        self.layout()
        # we only reset parent if the parent exists and
        # the flag to reset it is set.
        if changed and reset_parent:
            self.parent.reset_size(reset_parent)

    def delete(self):
        if self.is_loaded:
            self.unload()
        self.parent = None
        Managed.delete(self)


class Controller(Managed):
    def __init__(self):
        Managed.__init__(self)

    def set_manager(self, manager):
        Managed.set_manager(self, manager)
        manager.add_controller(self)

    def delete(self):
        self._manager.remove_controller(self)
        super().delete()


class Manager:
    def __init__(self):
        self.controllers = []  # list of controllers.

        self._hover = None  # the control that is being hovered
        self._focus = None  # the control that has the focus

        self.wheel_target = None  # the primary control to receive wheel events.
        self.wheel_hint = None    # the secondary control to receive wheel events.

    def add_controller(self, controller):
        assert controller not in self.controllers
        self.controllers.append(controller)

    def remove_controller(self, controller):
        assert controller in self.controllers
        self.controllers.remove(controller)
        if self._hover == controller:
            self.set_hover(None)
        if self._focus == controller:
            self.set_focus(None)

    def set_next_focus(self, direction):
        assert direction in [-1, 1]

        # all the focusable controllers
        focusable = [x for x in self.controllers if hasattr(x, 'on_gain_focus')]
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
            return True  # we only change focus on the dialog we are in.

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
        for control in self.controllers:
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
        if self.wheel_target in self.controllers:
            return self.wheel_target.on_mouse_scroll(x, y, scroll_x, scroll_y)
        elif self.wheel_hint in self.controllers:
            return self.wheel_hint.on_mouse_scroll(x, y, scroll_x, scroll_y)
        else:
            return True

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
        self.controllers = []
        self._focus = None
        self._hover = None
        self.wheel_hint = None
        self.wheel_target = None
