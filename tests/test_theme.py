import unittest

import pyglet

from pyglet_gui.theme import Theme


class TestTheme(unittest.TestCase):
    """
    Tests basic functionality of theme such as
    initializing a theme and generating graphical elements.
    """
    def test_access(self):
        theme = Theme({'first depth': {
            'second depth': [0, 0, 0, 0]
        }}, 'some_path')

        # test access by dict of dicts
        self.assertEqual(theme['first depth']['second depth'], [0, 0, 0, 0])

        # test access by path
        path = ['first depth', 'second depth']
        self.assertEqual(theme[path], [0, 0, 0, 0])

    def test_update(self):
        theme = Theme({'first depth': {
            'second depth': [0, 0, 0, 0]
        }}, 'some_path')

        update = {'first depth': {'second depth': [1, 1, 1, 1]}}
        theme.update(update)

        # test the theme was updated
        path = ['first depth', 'second depth']
        self.assertEqual(theme[path], [1, 1, 1, 1])

    def test_update_depth(self):
        theme = Theme({'first depth': {
            'second depth': [0, 0, 0, 0]
        }}, 'some_path')

        update = {'first depth': {'other second depth': [1, 1, 1, 1]}}
        theme.update(update)

        # test that theme was updated
        path = ['first depth', 'other second depth']
        self.assertEqual(theme[path], [1, 1, 1, 1])

    def test_load_texture(self):
        theme = Theme({'first depth': {'image': 'panel.png'}}, 'theme')

        # panel is an 32x32 image.
        self.assertEqual(theme['first depth']['image'].width, 32)
        self.assertEqual(theme['first depth']['image'].height, 32)

    def test_load_texture_with_dictionary(self):
        theme = Theme({'first depth': {'image': {'source': 'panel.png'}}}, 'theme')

        # panel is a 32x32 image.
        self.assertEqual(theme['first depth']['image'].width, 32)
        self.assertEqual(theme['first depth']['image'].height, 32)

    def test_load_texture_with_region(self):
        theme = Theme(
            {'first depth':
                 {'image':
                      {'source': 'panel.png', 'region': [0, 0, 16, 16]}
                 }
            }, 'theme')

        # region is a 16x16 image.
        self.assertEqual(theme['first depth']['image'].width, 16)
        self.assertEqual(theme['first depth']['image'].height, 16)

    def test_load_frame(self):
        theme = Theme(
            {'first depth':
                 {'image':
                      {'source': 'panel.png', 'frame': [8, 8, 16, 16]}
                 }
            }, 'theme')

        # panel is an 32x32 image.
        self.assertEqual(theme['first depth']['image'].width, 32)
        self.assertEqual(theme['first depth']['image'].height, 32)

    def test_update_with_texture(self):
        theme = Theme({'first depth': {'image': 'panel.png'}}, 'theme')

        update = {'first depth':
                      {'image':
                           {'source': 'panel.png', 'region': [0, 0, 16, 16]}
                      }
        }
        theme.update(update)

        # update is to a 16x16 image.
        self.assertEqual(theme['first depth']['image'].width, 16)
        self.assertEqual(theme['first depth']['image'].height, 16)


class TestLoadGraphics(unittest.TestCase):

    def setUp(self):
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)

        self.texture_theme = Theme({'image': 'panel.png'}, 'theme')
        self.texture_region_theme = Theme({'image': {'source': 'panel.png', 'region': [0, 0, 16, 16]}}, 'theme')
        self.frame_theme = Theme({'image': {'source': 'panel.png', 'frame': [8, 8, 16, 16]}}, 'theme')

    def test_load_texture(self):

        texture = self.texture_theme['image'].generate(color=[255, 255, 255, 255],
                                                       batch=self.batch,
                                                       group=self.group)
        self.batch.draw()

        self.assertEqual(texture.width, 32)
        self.assertEqual(texture.height, 32)

    def test_load_texture_region(self):

        texture = self.texture_region_theme['image'].generate(color=[255, 255, 255, 255],
                                                              batch=self.batch,
                                                              group=self.group)
        self.batch.draw()

        self.assertEqual(texture.width, 16)
        self.assertEqual(texture.height, 16)

    def test_load_frame(self):

        texture = self.frame_theme['image'].generate(color=[255, 255, 255, 255],
                                                     batch=self.batch,
                                                     group=self.group)
        self.batch.draw()

        self.assertEqual(texture.width, 32)
        self.assertEqual(texture.height, 32)


if __name__ == "__main__":
    unittest.main()
