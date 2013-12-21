from collections import OrderedDict

from pyglet_gui.core import Controller


class TwoStateController(Controller):
    def __init__(self, is_pressed=False, on_press=None):
        Controller.__init__(self)

        self._is_pressed = is_pressed
        self._on_press = lambda y: y
        if on_press is not None:
            self._on_press = on_press

    @property
    def is_pressed(self):
        return self._is_pressed

    def change_state(self):
        self._is_pressed = not self._is_pressed
        self._on_press(self._is_pressed)


class ContinuousStateController(Controller):
    def __init__(self, value=0.0, min_value=0.0, max_value=1.0, on_set=None):
        assert min_value <= value <= max_value
        Controller.__init__(self)

        self._min_value = min_value
        self._max_value = max_value
        self._value = value

        # a callback when the value is set.
        if on_set is None:
            self._on_set = lambda x: x
        else:
            self._on_set = on_set

    def set_value(self, value):
        assert self._min_value <= value <= self._max_value
        self._value = value
        self._on_set(value)

    @property
    def value(self):
        return self._value


class Option(Controller):
    def __init__(self, name, parent):
        Controller.__init__(self)
        self._option_name = name
        self._selector = parent

    def select(self):
        self._selector.deselect()
        self._selector.select(self._option_name)


class Selector:
    def __init__(self, options, labels=None, on_select=None, selected=None):
        assert len(options) > 0
        assert None not in options
        assert labels is None or len(options) == len(labels)
        assert selected is None or selected in options

        if labels is None:
            labels = options

        self._selected = selected

        widget_options = self._make_options(options, labels)
        self._options = OrderedDict(list(zip(options, widget_options)))

        self._on_select = lambda x: x
        if on_select is not None:
            self._on_select = on_select

    def _make_options(self, options, labels):
        # has to be implemented.
        raise NotImplementedError

    def select(self, option_name):
        if self._selected is not None:
            self._options[self._selected].change_state()
        self._selected = option_name
        self._options[option_name].change_state()
        self._on_select(option_name)

    def deselect(self):
        if self._selected is not None:
            self._options[self._selected].change_state()
        self._selected = None
