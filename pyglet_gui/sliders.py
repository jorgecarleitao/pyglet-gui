from pyglet_gui.controllers import ContinuousStateController
from pyglet_gui.core import Viewer


class Slider(ContinuousStateController, Viewer):
    PATH = 'slider'
    IMAGE_BAR = 'bar'
    IMAGE_KNOB = 'knob'
    IMAGE_STEP = 'step'

    def __init__(self, value=0.0, min_value=0.0, max_value=1.0, on_set=None, steps=None, width=0, height=0):
        ContinuousStateController.__init__(self, value=value,
                                           min_value=min_value,
                                           max_value=max_value,
                                           on_set=on_set)
        Viewer.__init__(self, width, height)

        self._bar = None    # a bar where the knob slides.
        self._knob = None   # the knob that moves along the bar.
        self._offset = (0, 0)  # offset of the knob image to its central position
        self._padding = (0, 0, 0, 0)  # padding of the bar image to its central position

        self.steps = steps
        self._markers = []  # markers in case of discrete steps.
        self._step_offset = (0, 0)

    def get_path(self):
        return self.PATH

    def load_graphics(self):
        theme = self.theme[self.get_path()]
        color = theme['gui_color']

        self._bar = theme[self.IMAGE_BAR]['image'].generate(color, **self.get_batch('foreground'))
        self._padding = theme[self.IMAGE_BAR]['padding']

        self._knob = theme[self.IMAGE_KNOB]['image'].generate(color, **self.get_batch('highlight'))
        self._offset = theme[self.IMAGE_KNOB]['offset']

        if self.steps is not None:
            image_path = self.IMAGE_STEP
            for n in range(0, self.steps + 1):
                self._markers.append(theme[image_path]['image'].generate(color, **self.get_batch('background')))
            self._step_offset = theme[image_path]['offset']

    def unload_graphics(self):
        self._knob.unload()
        self._bar.unload()

        for marker in self._markers:
            marker.unload()
        self._markers = []

    def hit_test(self, x, y):
        return self.is_inside(x, y)

    def set_knob_pos(self, pos):
        """
        A setter for value, but using normalized values.
        """
        pos = max(min(pos, 1.0), 0.0)

        self.set_value(self._min_value + (self._max_value - self._min_value) * pos)
        if self._bar is not None and self._knob is not None:
            x, y, width, height = self._bar.get_content_region()
            offset_x, offset_y = self._offset
            self._knob.update(x + int(width * pos) + offset_x,
                              y + offset_y,
                              self._knob.width, self._knob.height)

    def _knob_pos(self):
        """
        The position of the knob in the bar computed by our value.
        """
        return max(min(float(self._value - self._min_value) / (self._max_value - self._min_value), 1.0), 0.0)

    def _snap_to_nearest(self):
        """
        Snaps the knob and value to a discrete value dictated by steps.
        """
        assert self.steps is not None
        pos = float(int(self._knob_pos() * self.steps + 0.5))/self.steps

        self.set_knob_pos(pos)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        raise NotImplementedError

    def on_mouse_press(self, x, y, button, modifiers):
        return self.on_mouse_drag(x, y, 0, 0, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.steps is not None:
            self._snap_to_nearest()

    def delete(self):
        ContinuousStateController.delete(self)
        Viewer.delete(self)


class HorizontalSlider(Slider):
    def __init__(self, value=0.0, min_value=0.0, max_value=1.0, steps=None,
                 width=100, on_set=None):
        Slider.__init__(self, value=value,
                        min_value=min_value,
                        max_value=max_value,
                        steps=steps,
                        on_set=on_set)

        self.min_width = width

    def layout(self):
        left, right, top, bottom = self._padding
        self._bar.update(self.x + left, self.y + bottom,
                         self.width - left - right,
                         self.height - top - bottom)

        x, y, width, height = self._bar.get_content_region()

        # knob is positioned with an (x,y) offset
        # since its graphics are on its bottom-left corner.
        offset_x, offset_y = self._offset
        self._knob.update(x + int(width * self._knob_pos()) + offset_x,
                          y + offset_y,
                          self._knob.width, self._knob.height)

        if self.steps is not None:
            step = float(width) / self.steps
            offset_x, offset_y = self._step_offset
            for n in range(0, self.steps + 1):
                self._markers[n].update(int(x + step * n) + offset_x,
                                        y + offset_y,
                                        self._markers[n].width,
                                        self._markers[n].height)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        bar_x, bar_y, bar_width, bar_height = self._bar.get_content_region()
        self.set_knob_pos(float(x - bar_x) / bar_width)
        return True

    def compute_size(self):
        width, height = self._bar.get_needed_size(self.min_width, 0)
        left, right, top, bottom = self._padding

        return width + left + right, height + top + bottom
