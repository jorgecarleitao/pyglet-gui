from pyglet_gui.sliders import Slider


class ScrollBar(Slider):
    """
    An abstract scrollbar with a specific knob size to be set.
    """
    def __init__(self, width, height):
        Slider.__init__(self, width=width, height=height)

        # the size of the knob. Value runs from [_knob_size/2, 1 - _knob_size/2]
        self._knob_size = 0.0

        self._scrolled = 0  # a cumulative value of scroll to avoid re-layout on every scroll event.

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def re_layout(self):
        self.layout()
        # when we layout, we ask the parent also re_layout since
        # a scrollbar defines the content region.
        if self._scrolled > 2:
            self.parent.layout()
            self._scrolled = 0

    def _get_bar_region(self):
        """
        Returns the area of the space where the knob moves (x, y, width, height)
        """
        return self.x, self.y, self.width, self.height

    def _get_knob_region(self):
        """
        Returns the area of the knob (x, y, width, height). To be subclassed.
        """
        raise NotImplementedError

    def get_knob_pos(self):
        """
        Returns the position of the relative position of the knob
        in the bar.
        """
        raise NotImplementedError

    def set_knob_pos(self, pos):
        pos = max(min(pos, 1 - self._knob_size/2), self._knob_size/2)

        self._value = self._min_value + (self._max_value - self._min_value) * pos

    def layout(self):
        self._knob.update(*self._get_knob_region())
        self._bar.update(*self._get_bar_region())

    def on_gain_focus(self):
        if self._manager is not None:
            self._manager.set_wheel_target(self)

    def on_lose_focus(self):
        self._scrolled = 0
        if self._manager is not None:
            self._manager.set_wheel_target(None)


class HScrollbar(ScrollBar):
    PATH = 'hscrollbar'

    def __init__(self, width):
        ScrollBar.__init__(self, width=width, height=0)

    def _get_knob_region(self):
        return int(self.x + (self._knob_pos() - self._knob_size/2) * self.width), \
               self.y, int(self._knob_size * self.width), self.height

    def get_knob_pos(self):
        return int((self._knob_pos() - self._knob_size/2) * self.width)

    def load_graphics(self):
        super(HScrollbar, self).load_graphics()
        self.height = self._bar.height

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        bar_x, _, bar_width, _ = self._bar.get_content_region()

        absolute_distance = float(x - bar_x)
        relative_distance = absolute_distance/bar_width

        self.set_knob_pos(relative_distance)
        self._scrolled = 10
        self.re_layout()
        return True

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._scrolled += abs(scroll_x)
        self.set_knob_pos(self._knob_pos() - float(scroll_x) / self.width)
        self.re_layout()
        return True

    def set_knob_size(self, width, max_width):
        self._knob_size = float(width)/max_width

        # update the knob position given the new knob size.
        self.set_knob_pos(self._knob_pos())

    def compute_size(self):
        return self.width, self._bar.height


class VScrollbar(ScrollBar):
    PATH = 'vscrollbar'

    def __init__(self, height):
        ScrollBar.__init__(self, width=0, height=height)

    def _get_knob_region(self):
        top = self.y + self.height
        return (self.x, int(top - (self._knob_pos() + self._knob_size/2) * self.height),
                self.width, int(self._knob_size * self.height))

    def get_knob_pos(self):
        # we remove half the knob size to pick the center of the knob.
        # height/_knob_size = max_height by "set_knob_size()".
        return int((self._knob_pos() - self._knob_size/2) * self.height/self._knob_size)

    def load_graphics(self):
        super(VScrollbar, self).load_graphics()
        self.width = self._bar.width

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        bar_x, bar_y, bar_width, bar_height = self._bar.get_content_region()

        absolute_distance = float(y - bar_y)
        relative_distance = absolute_distance/bar_height
        self.set_knob_pos(1 - relative_distance)
        self._scrolled = 10
        self.re_layout()
        return True

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._scrolled += abs(scroll_y)
        self.set_knob_pos(self._knob_pos() + float(scroll_y) / self.height)
        self.re_layout()
        return True

    def set_knob_size(self, height, max_height):
        self._knob_size = float(height)/max_height

        # update the knob position given the new knob size.
        self.set_knob_pos(self._knob_pos())

    def compute_size(self):
        return self._bar.width, self.height
