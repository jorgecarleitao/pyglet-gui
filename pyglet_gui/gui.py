from pyglet_gui.widgets import Graphic, Label
from pyglet_gui.controllers import Controller
from pyglet_gui.containers import HorizontalContainer, VerticalContainer, Frame
from pyglet_gui.constants import VALIGN_BOTTOM, HALIGN_LEFT, HALIGN_CENTER
from pyglet_gui.dialog import Dialog
from pyglet_gui.buttons import Button


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

        self.folding_content.set_manager(manager)
        self.folding_content.parent = self

        self.header.set_manager(manager)
        self.header.parent = self

        for item in self._content:
            if item in [self.folding_content, self.header]:
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


class PopupMessage(Dialog):
    """A simple fire-and-forget dialog."""

    def __init__(self, text="", window=None, batch=None, group=None,
                 theme=None, on_escape=None):
        def on_ok(dialog=None):
            if on_escape is not None:
                on_escape(self)
            self.delete()

        Dialog.__init__(self, content=Frame(VerticalContainer([Label(text),
                                                            Button("Ok", on_press=on_ok)])),
                        window=window, batch=batch, group=group,
                        theme=theme, movable=True,
                        on_enter=on_ok, on_escape=on_ok)


class PopupConfirm(Dialog):
    """An ok/cancel-style dialog.  Escape defaults to cancel."""

    def __init__(self, text="", ok="Ok", cancel="Cancel",
                 window=None, batch=None, group=None, theme=None,
                 on_ok=None, on_cancel=None):
        def on_ok_click(dialog=None):
            if on_ok is not None:
                on_ok(self)
            self.delete()

        def on_cancel_click(dialog=None):
            if on_cancel is not None:
                on_cancel(self)
            self.delete()

        Dialog.__init__(self, content=Frame(
            VerticalContainer([
                Label(text),
                HorizontalContainer([
                    Button(ok, on_press=on_ok_click),
                    None,
                    Button(cancel, on_press=on_cancel_click)]),
                ])),
                        window=window, batch=batch, group=group,
                        theme=theme, movable=True,
                        on_escape=on_cancel_click)
