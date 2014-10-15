from abc import abstractmethod

import pyglet
from pyglet import gl
from ..core import Rectangle


class ThemeTextureGroup(pyglet.graphics.TextureGroup):
    """
    ThemeTextureGroup, in addition to setting the texture, also ensures that
    we map to the nearest texel instead of trying to interpolate from nearby
    texels. This prevents 'blooming' along the edges.
    """

    def set_state(self):
        super(ThemeTextureGroup, self).set_state()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)


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
