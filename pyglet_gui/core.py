from abc import ABCMeta, abstractmethod
import pyglet


class Managed(metaclass=ABCMeta):
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


class Viewer(Managed, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, widget):
        self._parent = widget

    @abstractmethod
    def load(self):
        # used to load graphics.
        pass

    @abstractmethod
    def unload(self):
        # used to unload graphics.
        pass

    def reload(self):
        self.unload()
        self.load()

    @abstractmethod
    def compute_size(self):
        pass

    @abstractmethod
    def set_position(self, x, y):
        # put this element in a new position
        pass

    def is_expandable(self):
        return False

    def expand(self, width, height):
        pass

    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def layout(self):
        # used to layout the children or graphics of the viewer in position
        pass

    def delete(self):
        self.unload()
        Managed.delete(self)


class Controller(Managed, metaclass=ABCMeta):
    def __init__(self):
        Managed.__init__(self)

    def set_manager(self, manager):
        Managed.set_manager(self, manager)
        manager.add_controller(self)

    def delete(self):
        self._manager.remove_controller(self)
        super().delete()


class Manager(pyglet.event.EventDispatcher):
    def __init__(self):
        pyglet.event.EventDispatcher.__init__(self)
        self.controllers = []  # list of controllers.
        self.hover = None  # the control that is being hovered
        self.focus = None  # the control that has the focus
        self.wheel_target = None  # the primary control to receive wheel events.
        self.wheel_hint = None    # the secondary control to receive wheel events.

    def add_controller(self, controller):
        assert controller not in self.controllers
        self.controllers.append(controller)

    def remove_controller(self, controller):
        assert controller in self.controllers
        self.controllers.remove(controller)
        if self.hover == controller:
            self.set_hover(None)
        if self.focus == controller:
            self.set_focus(None)

    def set_next_focus(self, direction):
        assert direction in [-1, 1]

        # all the focusable controllers
        focusable = [x for x in self.controllers if hasattr(x, 'on_gain_focus')]
        if not focusable:
            return

        if self.focus is not None and self.focus in focusable:
            index = focusable.index(self.focus)
        else:
            index = 0 - direction

        new_focus = focusable[(index + direction) % len(focusable)]
        self.set_focus(new_focus)

    def on_key_press(self, symbol, modifiers):
        ## move between focusable widgets.
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                direction = -1
            else:
                direction = 1

            self.set_next_focus(direction)
            return True  # we only change focus on the dialog we are in.

        if self.focus is not None and hasattr(self.focus, 'on_key_press'):
            return self.focus.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if self.focus is not None and hasattr(self.focus, 'on_key_release'):
            return self.focus.on_key_release(symbol, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus is not None and hasattr(self.focus, 'on_mouse_drag'):
            return self.focus.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        new_hover = None
        for control in self.controllers:
            if control.hit_test(x, y):
                new_hover = control
                break
        self.set_hover(new_hover)

        if self.hover is not None and hasattr(self.hover, 'on_mouse_motion'):
            return self.hover.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_focus(self.hover)
        if self.focus and hasattr(self.focus, 'on_mouse_press'):
            return self.focus.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.focus is not None and hasattr(self.focus, 'on_mouse_release'):
            return self.focus.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.wheel_target in self.controllers:
            return self.wheel_target.on_mouse_scroll(x, y, scroll_x, scroll_y)
        elif self.wheel_hint in self.controllers:
            return self.wheel_hint.on_mouse_scroll(x, y, scroll_x, scroll_y)
        else:
            return True

    def on_text(self, text):
        if self.focus and text != '\r' and hasattr(self.focus, 'on_text'):
            return self.focus.on_text(text)

    def on_text_motion(self, motion):
        if self.focus and hasattr(self.focus, 'on_text_motion'):
            return self.focus.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus and hasattr(self.focus, 'on_text_motion_select'):
            return self.focus.on_text_motion_select(motion)

    def set_focus(self, focus):
        if self.focus == focus:
            return
        if self.focus is not None and hasattr(self.focus, 'on_lose_focus'):
            self.focus.on_lose_focus()
        self.focus = focus
        if focus is not None and hasattr(self.focus, 'on_gain_focus'):
            self.focus.on_gain_focus()

    def set_hover(self, hover):
        if self.hover == hover:
            return
        if self.hover is not None and hasattr(self.hover, 'on_lose_highlight'):
            self.hover.on_lose_highlight()
        self.hover = hover
        if hover is not None and hasattr(self.hover, 'on_gain_highlight'):
            hover.on_gain_highlight()

    def set_wheel_hint(self, control):
        self.wheel_hint = control

    def set_wheel_target(self, control):
        self.wheel_target = control

    def delete(self):
        self.controllers = []
        self.focus = None
        self.hover = None
        self.wheel_hint = None
        self.wheel_target = None
