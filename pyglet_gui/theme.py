from abc import ABCMeta, abstractmethod
import json

import pyglet
from pyglet import gl

from pyglet_gui.core import Rectangle


class ThemeTextureGroup(pyglet.graphics.TextureGroup):
    """
    ThemeTextureGroup, in addition to setting the texture, also ensures that
    we map to the nearest texel instead of trying to interpolate from nearby
    texels. This prevents 'blooming' along the edges.
    """

    def set_state(self):
        super().set_state()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)


class GraphicElementTemplate(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, color, batch, group):
        return GraphicElement(color, batch, group)


class TextureGraphicElementTemplate(GraphicElementTemplate):
    def __init__(self, texture, width=None, height=None):
        GraphicElementTemplate.__init__(self)

        self.texture = texture
        self.width = width or texture.width
        self.height = height or texture.height

    def generate(self, color, batch, group):
        return TextureGraphicElement(self.texture, color, batch, group)


class FrameTextureGraphicElementTemplate(TextureGraphicElementTemplate):
    def __init__(self, texture, frame, padding, width=None, height=None):

        TextureGraphicElementTemplate.__init__(self, texture, width=width, height=height)
        self._frame_texture = texture.get_region(*frame).get_texture()
        x, y, width, height = frame
        self._margins = (x, texture.width - width - x,    # left, right
                         texture.height - height - y, y)  # top, bottom
        self._padding = padding

    def generate(self, color, batch, group):
        return FrameTextureGraphicElement(
            self.texture, self._frame_texture,
            self._margins, self._padding, color, batch, group)


class GraphicElement(Rectangle):
    def __init__(self, color, batch, group, width=0, height=0):
        Rectangle.__init__(self, width=width, height=height)
        self._color = color
        self._batch = batch
        self._group = group
        self._vertex_list = None
        self._load()

    @abstractmethod
    def _load(self):
        assert self._vertex_list is None
        self._vertex_list = self._batch.add(12, gl.GL_LINES, self._group,
                                            ('v2i', self._get_vertices()),
                                            ('c4B', self._color * 12))

    @abstractmethod
    def _get_vertices(self):
        x1, y1 = int(self._x), int(self._y)
        x2, y2 = x1 + int(self.width), y1 + int(self.height)
        return (x1, y1, x2, y1, x2, y1, x2, y2,
                x2, y2, x1, y2, x1, y2, x1, y1,
                x1, y1, x2, y2, x1, y2, x2, y1)

    def unload(self):
        self._vertex_list.delete()
        self._vertex_list = None
        self._group = None

    def get_content_region(self):
        return self._x, self._y, self.width, self.height

    def get_content_size(self, width, height):
        return width, height

    def get_needed_size(self, content_width, content_height):
        return content_width, content_height

    def update(self, x, y, width, height):
        self.set_position(x, y)
        self.width, self.height = width, height

        if self._vertex_list is not None:
            self._vertex_list.vertices = self._get_vertices()


class TextureGraphicElement(GraphicElement):
    def __init__(self, texture, color, batch, group):
        self.texture = texture
        GraphicElement.__init__(self,
                                color,
                                batch,
                                ThemeTextureGroup(texture, group),
                                texture.width, texture.height)

    def _load(self):
        assert self._vertex_list is None
        self._vertex_list = self._batch.add(4, gl.GL_QUADS, self._group,
                                            ('v2i', self._get_vertices()),
                                            ('c4B', self._color * 4),
                                            ('t3f', self.texture.tex_coords))

    def _get_vertices(self):
        x1, y1 = int(self._x), int(self._y)
        x2, y2 = x1 + int(self.width), y1 + int(self.height)
        return x1, y1, x2, y1, x2, y2, x1, y2


class FrameTextureGraphicElement(GraphicElement):
    def __init__(self, outer_texture, inner_texture, margins, padding, color, batch, group):
        self.outer_texture = outer_texture
        self.inner_texture = inner_texture
        self.margins = margins
        self.padding = padding
        GraphicElement.__init__(self,
                                color,
                                batch,
                                ThemeTextureGroup(outer_texture, group),
                                outer_texture.width,
                                outer_texture.height)

    def _load(self):
        assert self._vertex_list is None

        # 36 vertices: 4 for each of the 9 rectangles.
        self._vertex_list = self._batch.add(36, gl.GL_QUADS, self._group,
                                            ('v2i', self._get_vertices()),
                                            ('c4B', self._color * 36),
                                            ('t2f', self._get_tex_coords()))

    def _get_tex_coords(self):
        x1, y1 = self.outer_texture.tex_coords[0:2]  # outer's lower left
        x4, y4 = self.outer_texture.tex_coords[6:8]  # outer's upper right
        x2, y2 = self.inner_texture.tex_coords[0:2]  # inner's lower left
        x3, y3 = self.inner_texture.tex_coords[6:8]  # inner's upper right
        return (x1, y1, x2, y1, x2, y2, x1, y2,  # bottom left
                x2, y1, x3, y1, x3, y2, x2, y2,  # bottom
                x3, y1, x4, y1, x4, y2, x3, y2,  # bottom right
                x1, y2, x2, y2, x2, y3, x1, y3,  # left
                x2, y2, x3, y2, x3, y3, x2, y3,  # center
                x3, y2, x4, y2, x4, y3, x3, y3,  # right
                x1, y3, x2, y3, x2, y4, x1, y4,  # top left
                x2, y3, x3, y3, x3, y4, x2, y4,  # top
                x3, y3, x4, y3, x4, y4, x3, y4)  # top right

    def _get_vertices(self):
        left, right, top, bottom = self.margins
        x1, y1 = int(self._x), int(self._y)
        x2, y2 = x1 + int(left), y1 + int(bottom)
        x3 = x1 + int(self.width) - int(right)
        y3 = y1 + int(self.height) - int(top)
        x4, y4 = x1 + int(self.width), y1 + int(self.height)
        return (x1, y1, x2, y1, x2, y2, x1, y2,  # bottom left
                x2, y1, x3, y1, x3, y2, x2, y2,  # bottom
                x3, y1, x4, y1, x4, y2, x3, y2,  # bottom right
                x1, y2, x2, y2, x2, y3, x1, y3,  # left
                x2, y2, x3, y2, x3, y3, x2, y3,  # center
                x3, y2, x4, y2, x4, y3, x3, y3,  # right
                x1, y3, x2, y3, x2, y4, x1, y4,  # top left
                x2, y3, x3, y3, x3, y4, x2, y4,  # top
                x3, y3, x4, y3, x4, y4, x3, y4)  # top right

    def get_content_region(self):
        left, right, top, bottom = self.padding
        return (self._x + left, self._y + bottom,
                self.width - left - right, self.height - top - bottom)

    def get_content_size(self, width, height):
        left, right, top, bottom = self.padding
        return width - left - right, height - top - bottom

    def get_needed_size(self, content_width, content_height):
        left, right, top, bottom = self.padding
        return (max(content_width + left + right, self.outer_texture.width),
                max(content_height + top + bottom, self.outer_texture.height))


class ScopedDict(dict):
    """
    ScopedDict is a special type of dict with two additional features:
    - It is 'scoped' - if a key exists in a parent ScopedDict but
    not in the child ScopedDict, it returns the parent value.
    -  keys can be a list such that:
        sdict[['button', 'down', 'highlight']] is equivalent
        to sdict['button']['down']['highlight'].
    """

    def __init__(self, arg=None, parent=None):
        if arg is None:
            arg = {}
        super().__init__()
        self.parent = parent
        for k, v in arg.items():
            if isinstance(v, dict):
                self[k] = ScopedDict(v, self)
            else:
                self[k] = v

    def __getitem__(self, key):
        if key is None:
            return self
        elif isinstance(key, list) or isinstance(key, tuple):
            if len(key) > 1:
                return self.__getitem__(key[0]).__getitem__(key[1:])  # start a recursion
            elif len(key) == 1:
                return self.__getitem__(key[0])
            else:
                return self  # theme[][key] returns theme[key]
        else:
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                if self.parent is not None:
                    return self.parent.__getitem__(key)
                else:
                    raise

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            dict.__setitem__(self, key, ScopedDict(value, self))
        else:
            dict.__setitem__(self, key, value)

    def get(self, key, default=None):
        if isinstance(key, list) or isinstance(key, tuple):
            if len(key) > 1:
                return self.__getitem__(key[0]).get(key[1:], default)
            elif len(key) == 1:
                return self.get(key[0], default)
            else:
                raise KeyError(key)  # empty list

        if key in self:
            return dict.get(self, key)
        elif self.parent:
            return self.parent.get(key, default)
        else:
            return default

    def get_path(self, path, default=None):
        assert isinstance(path, list) or isinstance(path, tuple)
        if len(path) == 1:
            return self.get(path[0], default)
        else:
            return self.__getitem__(path[0]).get_path(path[1:], default)

    def set_path(self, path, value):
        assert isinstance(path, list) or isinstance(path, tuple)
        if len(path) == 1:
            return self.__setitem__(path[0], value)
        else:
            return self.__getitem__(path[0]).set_path(path[1:], value)


class Theme(ScopedDict):
    """
    A theme is a scoped dictionary that
    maps specific keys to specific templates.
    It is initialized by a dictionary (json-like) and by a resource path.
    It maps resources in the dictionary to resources in the path,
    initializing the correct template accordingly.
    """
    def __init__(self, dictionary, resources_path):
        ScopedDict.__init__(self, dictionary, None)

        self.loader = pyglet.resource.Loader(resources_path)

        self._textures = {}
        self._update_with_images(self, dictionary)

    @property
    def resources_path(self):
        return self.loader.path

    @resources_path.setter
    def resources_path(self, path):
        self.loader = pyglet.resource.Loader(path)

    def update(self, E=None, **F):
        super().update(E, **F)
        self._update_with_images(self, E)

    def _get_texture(self, filename):
        """
        Returns the texture associated with the filename. Loads it from
        resources if it haven't done before.
        """
        if filename not in self._textures:
            texture = self.loader.texture(filename)
            texture.src = filename
            self._textures[filename] = texture
        return self._textures[filename]

    def _get_texture_region(self, filename, x, y, width, height):
        """
        Same as _get_texture, but limits the texture for a region
        x, y, width, height.
        """
        texture = self._get_texture(filename)
        retval = texture.get_region(x, y, width, height).get_texture()
        retval.src = texture.src
        retval.region = [x, y, width, height]
        return retval

    def _update_with_images(self, target, input_dict):
        """
        The main function of theme. Called after initialization,
        it crawls the scoped dict and populates
        'target' with templates built from the dict.
        """
        for k, v in input_dict.items():
            if k.startswith('image'):
                if isinstance(v, dict):
                    width = height = None

                    # if it has a region, we create a texture from that region.
                    # else, we use a full texture.
                    if 'region' in v:
                        texture = self._get_texture_region(v['source'], *v['region'])
                    else:
                        texture = self._get_texture(v['source'])

                    # if it has frame, it is a FrameTexture
                    # else, it is a simple texture.
                    if 'frame' in v:
                        target[k] = FrameTextureGraphicElementTemplate(
                            texture,
                            v['frame'],
                            v.get('padding', [0, 0, 0, 0]),  # if padding, else 0.
                            width=width, height=height)
                    else:
                        target[k] = TextureGraphicElementTemplate(texture, width=width, height=height)
                else:
                    target[k] = TextureGraphicElementTemplate(self, self._get_texture(v))
            elif isinstance(v, dict):
                temp = ScopedDict(parent=target)
                self._update_with_images(temp, v)
                target[k] = temp
            else:
                target[k] = v


class ThemeFromPath(Theme):
    """
    A theme that is loaded from a json in a path.
    The convention is that the json file is called 'theme.json' and lives
    inside the resources_path given.
    """
    def __init__(self, resources_path):
        theme_file = pyglet.resource.Loader(resources_path).file('theme.json')
        try:
            dictionary = json.loads(theme_file.read().decode("utf-8"))
        finally:
            theme_file.close()
        super().__init__(dictionary, resources_path)
