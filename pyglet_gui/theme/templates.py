from abc import ABCMeta, abstractmethod

from .elements import GraphicElement, TextureGraphicElement, FrameTextureGraphicElement


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
        self._inner_texture = texture.get_region(*frame).get_texture()
        x, y, width, height = frame
        self._margins = (x, texture.width - width - x,    # left, right
                         texture.height - height - y, y)  # top, bottom
        self._padding = padding

    def generate(self, color, batch, group):
        return FrameTextureGraphicElement(
            self.texture, self._inner_texture,
            self._margins, self._padding, color, batch, group)
