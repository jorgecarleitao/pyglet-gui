import pyglet.text
from pyglet_gui.constants import VALIGN_BOTTOM, HALIGN_LEFT, HALIGN_CENTER, ANCHOR_CENTER, GetRelativePoint
from pyglet_gui.core import Rectangle, Viewer
from pyglet_gui.controllers import Controller
from pyglet_gui.containers import HorizontalContainer, VerticalContainer, Wrapper
from pyglet_gui.buttons import Button, FocusButton
from pyglet_gui.manager import Manager


class Graphic(Viewer):
    def __init__(self, path, is_expandable=False):
        Viewer.__init__(self)
        self._path = path
        self._expandable = is_expandable
        self._graphic = None
        self._min_width = self._min_height = 0

    def get_path(self):
        return self._path

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self._graphic = theme['image'].generate(theme[self._path]['gui_color'], **self.get_batch('background'))

        self._min_width = self._graphic.width
        self._min_height = self._graphic.height

    def unload_graphics(self):
        self._graphic.unload()

    def expand(self, width, height):
        assert self._expandable
        self.width, self.height = width, height
        self._graphic.update(self.x, self.y, self.width, self.height)

    def is_expandable(self):
        return self._expandable

    def layout(self):
        self._graphic.update(self.x, self.y, self.width, self.height)

    def compute_size(self):
        return self._min_width, self._min_height


class Label(Viewer):
    def __init__(self, text="", bold=False, italic=False,
                 font_name=None, font_size=None, color=None, path=None):
        Viewer.__init__(self)
        self.text = text
        self.bold = bold
        self.italic = italic
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.path = path
        self.label = None

    def get_path(self):
        return self.path

    def load_graphics(self):
        theme = self.theme[self.get_path()]

        self.label = pyglet.text.Label(self.text,
                                       bold=self.bold,
                                       italic=self.italic,
                                       color=self.color or theme['text_color'],
                                       font_name=self.font_name or theme['font'],
                                       font_size=self.font_size or theme['font_size'],
                                       **self.get_batch('background'))

    def unload_graphics(self):
        self.label.delete()

    def layout(self):
        font = self.label.document.get_font()
        self.label.x = self.x
        self.label.y = self.y - font.descent

    def set_text(self, text):
        self.text = text
        self.reload()
        self.reset_size()

    def compute_size(self):
        font = self.label.document.get_font()
        return self.label.content_width, font.ascent - font.descent


class Frame(Wrapper):
    """
    A Viewer that wraps another widget with a frame.
    """
    def __init__(self, content, path=None, image_name='image',
                 is_expandable=False, anchor=ANCHOR_CENTER):
        Wrapper.__init__(self, content, is_expandable=is_expandable, anchor=anchor)

        # private
        self._frame = None
        if path is None:
            self._path = ['frame']
        else:
            self._path = path
        self._image_name = image_name

    def get_path(self):
        return self._path

    def load_graphics(self):
        Wrapper.load_graphics(self)
        theme = self.theme[self.get_path()]
        if self._frame is None:
            template = theme[self._image_name]
            self._frame = template.generate(theme['gui_color'], **self.get_batch('panel'))

    def unload_graphics(self):
        if self._frame is not None:
            self._frame.unload()
            self._frame = None
        Wrapper.unload_graphics(self)

    def expand(self, width, height):
        if self.content.is_expandable():
            content_width, content_height = self._frame.get_content_size(width, height)
            self.content.expand(content_width, content_height)
        self.width, self.height = width, height

    def layout(self):
        self._frame.update(self.x, self.y, self.width, self.height)

        # we create a rectangle with the interior for using in GetRelativePoint
        x, y, width, height = self._frame.get_content_region()
        interior = Rectangle(x, y, width, height)
        x, y = GetRelativePoint(interior, self.anchor, self.content, self.anchor, self.content_offset)
        self.content.set_position(x, y)

    def compute_size(self):
        self.content.compute_size()
        return self._frame.get_needed_size(self.content.width, self.content.height)


class TitleFrame(VerticalContainer):
    def __init__(self, title, content):
        VerticalContainer.__init__(self, content=[
            HorizontalContainer([Graphic(path=["titlebar", "left"], is_expandable=True),
                                 Frame(Label(title, path=["titlebar"]),
                                       path=["titlebar", "center"]),
                                 Graphic(path=["titlebar", "right"], is_expandable=True),
                                 ], align=VALIGN_BOTTOM, padding=0),
            Frame(content, path=["titlebar", "frame"], is_expandable=True),
            ], padding=0)


class SectionHeader(HorizontalContainer):
    def __init__(self, title, align=HALIGN_CENTER):
        if align == HALIGN_LEFT:
            left_expand = False
            right_expand = True
        elif align == HALIGN_CENTER:
            left_expand = True
            right_expand = True
        else:  # HALIGN_RIGHT
            left_expand = True
            right_expand = False

        HorizontalContainer.__init__(self, content=[
            Graphic(path=["section", "left"], is_expandable=left_expand),
            Frame(Label(title, path=["section"]), path=['section', 'center']),
            Graphic(path=["section", "right"], is_expandable=right_expand),
            ], align=VALIGN_BOTTOM, padding=0)


class FoldingSection(VerticalContainer, Controller):
    def __init__(self, title, content=None, is_open=True, align=HALIGN_CENTER):
        Controller.__init__(self)
        if align == HALIGN_LEFT:
            left_expand = False
            right_expand = True
        elif align == HALIGN_CENTER:
            left_expand = True
            right_expand = True
        else:  # HALIGN_RIGHT
            left_expand = True
            right_expand = False

        self.is_open = is_open
        self.folding_content = content
        self.book = Graphic(self._get_image_path())

        self.header = HorizontalContainer([Graphic(path=["section", "left"], is_expandable=left_expand),
                                           Frame(HorizontalContainer([
                                               self.book,
                                               Label(title, path=["section"]),
                                               ]), path=["section", "center"]),
                                           Graphic(path=["section", "right"], is_expandable=right_expand),
                                           ], align=VALIGN_BOTTOM, padding=0)
        layout = [self.header]
        if self.is_open:
            layout.append(self.folding_content)

        VerticalContainer.__init__(self, content=layout, align=align)

    def set_manager(self, manager):
        Controller.set_manager(self, manager)

        self.header.set_manager(manager)
        self.header.parent = self

        for item in self._content:
            if item == self.header:
                continue
            item.set_manager(self._manager)
            item.parent = self

    def _get_image_path(self):
        if self.is_open:
            return ["section", "opened"]
        else:
            return ["section", "closed"]

    def hit_test(self, x, y):
        return self.header.is_inside(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.is_open = not self.is_open

        self.book._path = self._get_image_path()
        self.book.reload()

        if self.is_open:
            self.add(self.folding_content)
        else:
            self.remove(self.folding_content)

    def delete(self):
        if not self.is_open:
            self.folding_content.delete()
        self.folding_content = None
        VerticalContainer.delete(self)


class PopupMessage(Manager):
    """A simple fire-and-forget manager."""

    def __init__(self, text="", window=None, batch=None, group=None,
                 theme=None, on_escape=None, have_focus=False):
        def on_ok(_):
            if on_escape is not None:
                on_escape(self)
            self.delete()

        button = FocusButton("Ok", on_press=on_ok)
        Manager.__init__(self, content=Frame(VerticalContainer(
                         [Label(text), button])),
                         window=window, batch=batch, group=group,
                         theme=theme, is_movable=True)
        Manager.set_next_focus(self, 1)


class PopupConfirm(Manager):
    """An ok/cancel-style dialog.  Escape defaults to cancel."""

    def __init__(self, text="", ok="Ok", cancel="Cancel",
                 window=None, batch=None, group=None, theme=None,
                 on_ok=None, on_cancel=None):
        def on_ok_click(_):
            if on_ok is not None:
                on_ok(self)
            self.delete()

        def on_cancel_click(_):
            if on_cancel is not None:
                on_cancel(self)
            self.delete()

        Manager.__init__(self, content=Frame(
            VerticalContainer([
                Label(text),
                HorizontalContainer([Button(ok, on_press=on_ok_click),
                                     None,
                                     Button(cancel, on_press=on_cancel_click)]
                )])
        ), window=window, batch=batch, group=group, theme=theme, is_movable=True)
