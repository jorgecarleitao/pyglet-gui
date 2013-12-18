from functools import reduce

from pyglet_gui.constants import HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT, \
    VALIGN_TOP, VALIGN_CENTER, ANCHOR_CENTER, ANCHOR_TOP_LEFT, GetRelativePoint

from pyglet_gui.widgets import Widget, Spacer, Rectangle


class Container(Widget):
    def __init__(self, content, width=0, height=0):
        assert isinstance(content, list)
        super().__init__(width, height)
        self._content = [x or Spacer() for x in content]

    @property
    def content(self):
        return self._content

    def set_manager(self, manager):
        Widget.set_manager(self, manager)
        for item in self._content:
            item.set_manager(self._manager)
            item.parent = self

    def load(self):
        for item in self._content:
            item.load()

    def unload(self):
        for item in self._content:
            item.unload()

    def add(self, item):
        item = item or Spacer()
        assert isinstance(item, Widget)
        item.reload()
        item.reset_size()
        self._content.append(item)
        self.reset_size()

    def remove(self, item):
        assert isinstance(item, Widget)

        item.unload()
        self._content.remove(item)
        self.reset_size()

    def delete(self):
        for item in self._content:
            item.delete()
        self._content = []
        Widget.delete(self)

    def set(self, content):
        self.unload()
        self._content = [x or Spacer() for x in content]
        for item in self._content:
            item.set_manager(self._manager)
        self.reset_size()

    def reset_size(self, reset_parent=True):
        if not reset_parent:
            for item in self._content:
                item.reset_size(reset_parent=False)
        super().reset_size(reset_parent)


class VerticalLayout(Container):
    def __init__(self, content=None, align=HALIGN_CENTER, padding=5):
        assert align in (HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT)
        super().__init__(content)
        self.align = align
        self.padding = padding
        self._expandable = []

    def expand(self, width, height):
        """
        Expands to fill available vertical space.  We split available space
        equally between all spacers.
        """
        available = int((height - self.height) / len(self._expandable))
        remainder = height - self.height - len(self._expandable) * available
        for item in self._expandable:
            if remainder > 0:
                item.expand(item.width, item.height + available + 1)
                remainder -= 1
            else:
                item.expand(item.width, item.height + available)
        self.height = height
        self.width = width

    def is_expandable(self):
        # True if we contain expandable content.
        return len(self._expandable) > 0

    def layout(self):
        # Expand any expandable content to our width
        for item in self._content:
            if item.is_expandable() and item.width < self.width:
                item.expand(self.width, item.height)

        top = self.y + self.height
        if self.align == HALIGN_RIGHT:
            for item in self._content:
                item.set_position(self.x + self.width - item.width, top - item.height)
                top -= item.height + self.padding
        elif self.align == HALIGN_CENTER:
            for item in self._content:
                item.set_position(self.x + self.width / 2 - item.width / 2, top - item.height)
                top -= item.height + self.padding
        else:  # HALIGN_LEFT
            for item in self._content:
                item.set_position(self.x, top - item.height)
                top -= item.height + self.padding

    def compute_size(self):
        if len(self._content) < 2:
            height = 0
        else:
            height = -self.padding
        width = 0
        for item in self._content:
            height += item.height + self.padding
            width = max(width, item.width)
        self._expandable = [x for x in self._content if x.is_expandable()]

        return width, height


class HorizontalLayout(Container):
    def __init__(self, content=None, align=VALIGN_CENTER, padding=5):
        assert align in (HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT)
        super().__init__(content)
        self.align = align
        self.padding = padding
        self._expandable = []

    def is_expandable(self):
        # True if we contain expandable content.
        return len(self._expandable) > 0

    def expand(self, width, height):
        """
        Expands to fill available horizontal space.  We split available space
        equally between all spacers.
        """
        available = int((width - self.width) / len(self._expandable))
        remainder = height - self.height - len(self._expandable) * available
        for item in self._expandable:
            if remainder > 0:
                item.expand(item.width + available + 1, item.height)
                remainder -= 1
            else:
                item.expand(item.width + available, item.height)
        self.width = width

    def layout(self):
        # Expand any expandable content to our height
        for item in self._content:
            if item.is_expandable() and item.height < self.height:
                item.expand(item.width, self.height)

        left = self.x
        if self.align == VALIGN_TOP:
            for item in self._content:
                item.set_position(left, self.y + self.height - item.height)
                left += item.width + self.padding
        elif self.align == VALIGN_CENTER:
            for item in self._content:
                item.set_position(left, self.y + self.height / 2 - item.height / 2)
                left += item.width + self.padding
        else:  # VALIGN_BOTTOM
            for item in self._content:
                item.set_position(left, self.y)
                left += item.width + self.padding

    def compute_size(self):
        height = 0
        if len(self._content) < 2:
            width = 0
        else:
            width = -self.padding
        for item in self._content:
            item.compute_size()
            height = max(height, item.height)
            width += item.width + self.padding
        self._expandable = [x for x in self._content if x.is_expandable()]

        return width, height


class GridLayout(Widget):
    """
    Arranges Widgets in a table.  Each cell's height and width are set to
    the maximum width of any Widget in its column, or the maximum height of
    any Widget in its row.

    Widgets are by default aligned to the top left corner of their cells.
    Another anchor point may be specified, i.e. ANCHOR_CENTER will ensure
    that Widgets are centered within cells.
    """

    def __init__(self, content=None, anchor=ANCHOR_TOP_LEFT, padding=5,
                 offset=(0, 0)):
        assert ((isinstance(content, list) or isinstance(content, tuple)) and
                (len(content) == 0 or (isinstance(content[0], list) or
                                       isinstance(content[0], tuple))))
        Widget.__init__(self)
        self._matrix = content  # a matrix-like list [[]]. Content can be None for cells without widgets.
        self.anchor = anchor
        self.padding = padding
        self.offset = offset

        self._max_heights = [0] * len(self._matrix)
        width = 0
        for row in self._matrix:
            width = max(width, len(row))
        self._max_widths = [self.padding] * width

    @property
    def content(self):
        return self._matrix

    def set_manager(self, manager):
        Widget.set_manager(self, manager)
        for row in self._matrix:
            for item in row:
                if item is not None:
                    item.set_manager(self._manager)
                    item.parent = self

    def load(self):
        for row in self._matrix:
            for item in row:
                if item is not None:
                    item.load()

    def unload(self):
        for row in self._matrix:
            for item in row:
                if item is not None:
                    item.unload()

    def add_row(self, row):
        """
        Adds a new row to the layout

        @param row An array of widgets, or None for cells without widgets
        """
        assert isinstance(row, tuple) or isinstance(row, list)
        for item in row:
            if item is not None:
                item.set_manager(self._manager)
                item.parent = self
        self._matrix.append(row)
        self.compute_size()

    def unload_row(self, row):
        """
        Unload a row from the layout
        """
        # todo: unclear why there is a pop in this method. Is not consistent with other unloads.
        if len(self._matrix) <= row:
            return
        row = self._matrix.pop(row)
        for column in row:
            if column is not None:
                column.unload()
        self.compute_size()

    def get(self, column, row):
        if row >= len(self._matrix):
            raise IndexError
        row = self._matrix[row]
        if column >= len(row):
            raise IndexError
        else:
            return row[column]

    def set(self, column, row, item):
        """
        Sets the content of a cell within the grid.
        """
        if len(self._matrix) <= row:
            self._matrix = list(self._matrix) + [] * (row - len(self._matrix) + 1)
        if len(self._matrix[row]) <= column:
            self._matrix[row] = list(self._matrix[row]) + [None] * (column - len(self._matrix[row]) + 1)
        if self._matrix[row][column] is not None:
            self._matrix[row][column].unload()
        self._matrix[row][column] = item
        item.set_manager(self._manager)
        self.compute_size()

    def layout(self):
        row_index = 0
        placement = Rectangle()
        placement.y = self.y + self.height
        for row in self._matrix:
            col_index = 0
            placement.x = self.x
            placement.height = self._max_heights[row_index]
            placement.y -= placement.height
            for item in row:
                placement.width = self._max_widths[col_index]
                if item is not None:
                    if item.is_expandable():
                        item.expand(placement.width, placement.height)
                    item.set_position(*GetRelativePoint(placement, self.anchor, item, self.anchor, self.offset))
                placement.x += placement.width
                col_index += 1
            row_index += 1

    def reset_size(self, reset_parent=True):
        if not reset_parent:
            for row in self._matrix:
                for item in row:
                    if item is not None:
                        item.reset_size(reset_parent=False)
        super().reset_size(reset_parent)

    def compute_size(self):
        # Recalculates our size and the maximum widths and heights of
        # each row and column.
        row_index = 0
        for row in self._matrix:
            max_height = self.padding
            col_index = 0
            for item in row:
                if item is not None:
                    item.compute_size()
                    width, height = item.width, item.height
                else:
                    width = height = 0
                max_height = max(max_height, height + self.padding)
                max_width = self._max_widths[col_index]
                max_width = max(max_width, width + self.padding)
                self._max_widths[col_index] = max_width
                col_index += 1
            self._max_heights[row_index] = max_height
            row_index += 1

        if self._max_widths:
            width = reduce(lambda x, y: x + y, self._max_widths) - self.padding
        else:
            width = 0
        if self._max_heights:
            height = reduce(lambda x, y: x + y, self._max_heights) - self.padding
        else:
            height = 0

        return width, height

    def delete(self):
        for row in self._matrix:
            for item in row:
                item.delete()
        self._matrix = []
        Widget.delete(self)


class FreeLayout(Spacer):
    """
    FreeLayout defines a rectangle on the screen where Widgets may be placed
    freely, in relation to one of its anchor points.  There is no constraints
    against the Widgets overlapping.

    FreeLayout will expand to fill available space in layouts; thus you could
    place a FreeLayout as one half of a VerticalLayout, lay out controls in
    the other half, and be assured the FreeLayout would be resized to the
    width of the overall Dialog.
    """

    def __init__(self, width=0, height=0, content=None):
        """
        Creates a new FreeLayout.

        :param width: Minimum width of FreeLayout area
        :param height: Minimum height of FreeLayout area
        :param content: A list of placement/Widget tuples, in the form:
                       [(ANCHOR_TOP_LEFT, 0, 0, YourWidget()),
                        (ANCHOR_TOP_RIGHT, 0, 0, YourWidget()),
                        (ANCHOR_CENTER, 30, -20, YourWidget())]
            where each tuple is (anchor, offset-x, offset-y, widget)
        """
        Spacer.__init__(self, width, height)
        self._content = content

    def set_manager(self, manager):
        Widget.set_manager(self, manager)
        for item in self._content:
            item.set_manager(self._manager)

    def add(self, anchor, x, y, widget):
        """
        Adds the Widget to the FreeLayout.

        :param anchor: Anchor point to set for the widget.
        :param x: X-coordinate of offset from anchor point; positive is to
                 the right.
        :param y: Y-coordinate of offset from anchor point; positive is upward.
        """
        self._content.append((anchor, x, y, widget))
        widget.set_manager(self._manager)
        widget.parent = self

    def layout(self):
        """
        Lays out Widgets within the FreeLayout. We make no attempt to
        assure there is enough space for them.
        """
        for anchor, offset_x, offset_y, widget in self._content:
            x, y = GetRelativePoint(self, anchor, widget, anchor, (offset_x, offset_y))
            widget.set_position(x, y)

    def remove(self, widget):
        self._content = [x for x in self._content if x[3] != widget]
        widget.delete()

    def compute_size(self):
        Spacer.compute_size(self)
        for _, _, _, widget in self._content:
            widget.compute_size()

    def delete(self):
        for _, _, _, item in self._content:
            item.delete()
        self._content = []
        Widget.delete(self)


class Wrapper(Widget):
    """
    A Widget that wraps another widget.
    """
    def __init__(self, content, is_expandable=False, anchor=ANCHOR_CENTER, offset=(0, 0)):
        Widget.__init__(self)
        self._content = content
        self._content.parent = self

        self.expandable = is_expandable

        self._anchor = anchor
        self.content_offset = offset

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor):
        self._anchor = anchor

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        assert isinstance(content, Widget)
        if self._content is not None:
            self._content.delete()

        self._content = content
        self._content.set_manager(self._manager)
        self._content.parent = self
        self.reset_size()

    def set_manager(self, manager):
        Widget.set_manager(self, manager)
        self._content.set_manager(manager)
        self._content.parent = self

    def load(self):
        self._content.load()

    def unload(self):
        self._content.unload()

    def expand(self, width, height):
        if self._content.is_expandable():
            self._content.expand(width, height)
        self.width = width
        self.height = height

    def is_expandable(self):
        return self.expandable

    def compute_size(self):
        return self._content.width, self._content.height

    def reset_size(self, reset_parent=True):
        if not reset_parent:
            self._content.reset_size(reset_parent)
        super().reset_size(reset_parent)

    def layout(self):
        x, y = GetRelativePoint(self, self.anchor, self._content, self.anchor, self.content_offset)
        self._content.set_position(x, y)

    def set_content(self, content):
        self._content.unload()
        self._content = content
        self._content.set_manager(self._manager)
        self._content.parent = self

    def delete(self):
        self._content.delete()
        Widget.delete(self)


class Frame(Wrapper):
    """
    A Widget that wraps another widget with a frame.
    """
    def __init__(self, content=None, path=None, image_name='image',
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

    def load(self):
        Wrapper.load(self)
        theme = self.theme[self.get_path()]
        if self._frame is None:
            template = theme[self._image_name]
            self._frame = template.generate(theme['gui_color'], **self.get_batch('panel'))

    def unload(self):
        if self._frame is not None:
            self._frame.unload()
            self._frame = None
        Wrapper.unload(self)

    def expand(self, width, height):
        if self._content.is_expandable():
            content_width, content_height = self._frame.get_content_size(width, height)
            self._content.expand(content_width, content_height)
        self.width, self.height = width, height

    def layout(self):
        self._frame.update(self.x, self.y, self.width, self.height)

        # we create a rectangle with the interior for using in GetRelativePoint
        x, y, width, height = self._frame.get_content_region()
        interior = Rectangle(x, y, width, height)
        x, y = GetRelativePoint(interior, self.anchor, self._content, self.anchor, self.content_offset)
        self._content.set_position(x, y)

    def compute_size(self):
        self._content.compute_size()
        return self._frame.get_needed_size(self._content.width, self._content.height)
