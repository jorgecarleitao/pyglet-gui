from abc import abstractmethod

import pyglet.resource

from .templates import TextureTemplate, FrameTextureTemplate


class Parser:

    @abstractmethod
    def condition_fulfilled(self, key):
        return False

    @abstractmethod
    def parse_element(self, element):
        pass


class TextureParser(Parser):

    def __init__(self, resources_path):
        self._textures = {}
        self._loader = pyglet.resource.Loader(resources_path)

    def condition_fulfilled(self, key):
        return key.startswith('image')

    def _get_texture(self, filename):
        """
        Returns the texture associated with the filename. Loads it from
        resources if it haven't done before.
        """
        if filename not in self._textures:
            texture = self._loader.texture(filename)
            self._textures[filename] = texture
        return self._textures[filename]

    def _get_texture_region(self, filename, x, y, width, height):
        """
        Same as _get_texture, but limits the texture for a region
        x, y, width, height.
        """
        texture = self._get_texture(filename)
        retval = texture.get_region(x, y, width, height).get_texture()
        return retval

    def parse_element(self, element):
        if isinstance(element, dict):
            # if it has a region, we create a texture from that region.
            # else, we use a full texture.
            if 'region' in element:
                texture = self._get_texture_region(element['source'], *element['region'])
            else:
                texture = self._get_texture(element['source'])

            # if it has frame, it is a FrameTexture
            # else, it is a simple texture.
            if 'frame' in element:
                return FrameTextureTemplate(
                    texture,
                    element['frame'],
                    element.get('padding', [0, 0, 0, 0])  # if padding, else 0.
                )
            else:
                return TextureTemplate(texture)
        # if it is of the form {'image': 'test.png'}
        else:
            texture = self._get_texture(element)
            return TextureTemplate(texture)
