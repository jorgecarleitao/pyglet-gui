import pyglet

from pyglet_gui.controllers import Option, Selector
from pyglet_gui.gui import Frame
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.constants import ANCHOR_TOP_LEFT, ANCHOR_BOTTOM_LEFT, HALIGN_CENTER, VALIGN_TOP
from pyglet_gui.manager import Manager
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.buttons import Button, OneTimeButton


class OptionButton(Option, Button):
    def __init__(self, option_name, button_text="", is_selected=False, parent=None):
        Option.__init__(self, option_name, parent)
        Button.__init__(self, label=button_text, is_pressed=is_selected)

    def expand(self, width, height):
        self.width = width
        self.height = height

    def is_expandable(self):
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        self.select()
        self.parent.layout()
        return True

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.select()
            self.parent.layout()
            return True


class VerticalButtonSelector(VerticalContainer, Selector):
    def __init__(self, options, labels=None, align=HALIGN_CENTER, padding=4, on_select=None):
        Selector.__init__(self, options, labels, on_select)
        VerticalContainer.__init__(self, list(self._options.values()), align=align, padding=padding)

    def _make_options(self, options, labels):
        widget_options = []
        for option, label in zip(options, labels):
            widget_options.append(OptionButton(option, label, is_selected=(option == self._selected), parent=self))
        return widget_options


class Dropdown(Selector, OneTimeButton):
    def __init__(self, options, labels=None, max_height=400, align=VALIGN_TOP, on_select=None):
        Selector.__init__(self, options, labels, on_select=on_select, selected=options[0])
        OneTimeButton.__init__(self)

        self.max_height = max_height
        self.align = align

        self._pulldown_menu = None

    def _make_options(self, options, labels):
        widget_options = []
        for option, label in zip(options, labels):
            widget_options.append(OptionButton(option, label, is_selected=(option == self._selected), parent=self))
        return widget_options

    def _delete_pulldown_menu(self):
        if self._pulldown_menu is not None:
            self._pulldown_menu.window.remove_handlers(self._pulldown_menu)
            self._pulldown_menu.delete()
            self._pulldown_menu = None

    def get_path(self):
        return 'dropdown'

    def load_graphics(self):
        self.label = self._options[self._selected].label
        OneTimeButton.load_graphics(self)

    def unload_graphics(self):
        OneTimeButton.unload_graphics(self)
        self._delete_pulldown_menu()

    def select(self, option_name):
        Selector.select(self, option_name)
        self._delete_pulldown_menu()
        self.reload()
        self.reset_size()
        self.layout()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        A mouse press is going to create a manager with the options.
        """
        # if it's already opened, we just close it.
        if self._pulldown_menu is not None:
            self._delete_pulldown_menu()
            return

        # the function we pass to the manager.
        def on_escape(_):
            self._delete_pulldown_menu()

        # Compute the anchor point and location for the manager
        width, height = self._manager.window.get_size()
        if self.align == VALIGN_TOP:
            # Dropdown is at the top, pulldown appears below it
            anchor = ANCHOR_TOP_LEFT
            x = self.x
            y = -(height - self.y - 1)
        else:
            # Dropdown is at the bottom, pulldown appears above it
            anchor = ANCHOR_BOTTOM_LEFT
            x = self.x
            y = self.y + self.height + 1

        # we set the manager
        self._pulldown_menu = Manager(
            Frame(Scrollable(VerticalContainer(list(self._options.values())),
                             height=self.max_height), path=['dropdown', 'pulldown']),
            window=self._manager.window, batch=self._manager.batch,
            group=self._manager.root_group.parent, theme=self._manager.theme,
            is_movable=False, anchor=anchor, offset=(x, y))

    def delete(self):
        self._delete_pulldown_menu()
        OneTimeButton.delete(self)
