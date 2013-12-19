from .setup import TestPygletGUI

from pyglet_gui.manager import Manager
from pyglet_gui.sliders import HorizontalSlider


class TestSlider(TestPygletGUI):

    def setUp(self):
        TestPygletGUI.setUp(self)
        self.slider = HorizontalSlider(min_value=0, max_value=10)
        self.manager = Manager(self.slider, window=self.window, batch=self.batch, theme=self.theme)

    def test_set_value(self):
        self.slider.set_knob_pos(0.5)
        self.assertEqual(self.slider.get_value(), 5)

    def test_mouse_slide(self):

        # push the slider to the minimum
        self.slider.on_mouse_press(0, 0, None, None)
        self.assertEqual(self.slider.get_value(), 0)

        # push the slider to the maximum
        self.slider.on_mouse_press(10000, 0, None, None)
        self.assertEqual(self.slider.get_value(), 10)

    def tearDown(self):
        self.manager.delete()
        super().tearDown()
