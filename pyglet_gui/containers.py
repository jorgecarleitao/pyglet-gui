from functools import reduce

from pyglet_gui.constants import HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT, \
    VALIGN_TOP, VALIGN_CENTER, ANCHOR_CENTER, GetRelativePoint

from pyglet_gui.core import Viewer, Rectangle


class Spacer(Viewer):
    def __init__(self, min_width=0, min_height=0):
        Viewer.__init__(self)
        self._min_width, self._min_height = min_width, min_height

    def expand(self, width, height):
        self.width, self.height = width, height

    def is_expandable(self):
        return True

    def compute_size(self):
        return self._min_width, self._min_height


class Container(Viewer):
    def __init__(self, content, width=0, height=0):
        assert isinstance(content, list)
        super(Container, self).__init__(width, height)
        self._content = [x or Spacer() for x in content]

    @property
    def content(self):
        return self._content

    def set_manager(self, manager):
        Viewer.set_manager(self, manager)
        for item in self._content:
            item.set_manager(self._manager)
            item.parent = self

    def load_content(self):
        for item in self._content:
            item.load()

    def load(self):
        super(Container, self).load()
        self.load_content()

    def unload_content(self):
        for item in self._content:
            item.unload()

    def unload(self):
        super(Container, self).unload()
        self.unload_content()

    def add(self, item, position=0):
        item = item or Spacer()
        assert isinstance(item, Viewer)

        item.set_manager(self._manager)
        item.parent = self

        item.load()
        item.reset_size()
        self._content.insert(len(self._content) - position, item)
        self.reset_size()

    def remove(self, item):
        assert isinstance(item, Viewer)
        item.unload()
        self._content.remove(item)

        item.delete()

        self.reset_size()

    def delete(self):
        for item in self._content:
            item.delete()
        self._content = []
        Viewer.delete(self)

    def reset_size(self, reset_parent=True):
        if not reset_parent:
            for item in self._content:
                item.reset_size(reset_parent=False)
        super(Container, self).reset_size(reset_parent)


class VerticalContainer(Container):
    def __init__(self, content, align=HALIGN_CENTER, padding=5):
        assert align in (HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT)
        super(VerticalContainer, self).__init__(content)
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
        # True if we contain an expandable content.
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


class HorizontalContainer(Container):
    def __init__(self, content, align=VALIGN_CENTER, padding=5):
        assert align in (HALIGN_CENTER, HALIGN_LEFT, HALIGN_RIGHT)
        super(HorizontalContainer, self).__init__(content)
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


class GridContainer(Container):
    """
    Arranges Widgets in a table.  Each cell's height and width are set to
    the maximum width of any Viewer in its column, or the maximum height of
    any Viewer in its row.
    """
    def __init__(self, content, anchor=ANCHOR_CENTER, padding=5,
                 offset=(0, 0)):
        assert isinstance(content, list) and len(content) != 0
        # todo: transform all "None" in "Spacers".

        # we set _content to be a flatten list of content.
        Container.__init__(self, [item for sub_list in content for item in sub_list])

        # and we set _matrix to be the matrix-like list [[]].
        self._matrix = content
        self.anchor = anchor
        self.padding = padding
        self.offset = offset

        self._max_heights = []
        self._max_widths = []
        self._update_max_vectors()

    @property
    def content(self):
        return self._matrix

    def _update_max_vectors(self):
        """
        Updates the sizes of vectors _max_widths and _max_heights.

        Must be called when _matrix changes number of elements.
        """
        # re-compute length of vector _max_widths
        self._max_heights = [0] * len(self._matrix)
        width = 0
        for row in self._matrix:
            width = max(width, len(row))
        self._max_widths = [0] * width

    def add_row(self, row):
        """
        Adds a new row to the layout.
        """
        assert isinstance(row, list)
        for item in row:
            item = item or Spacer()
            item.set_manager(self._manager)
            item.parent = self
            item.load()
            self._content.append(item)
        self._matrix.append(row)

        self._update_max_vectors()

        self.reset_size()

    def add_column(self, column):
        """
        Adds a new column to the layout.
        """
        assert isinstance(column, list)

        # assign items parents and managers
        for item in column:
            if item is not None:
                item = item or Spacer()
                item.set_manager(self._manager)
                item.parent = self
                item.load()
                self._content.append(item)

        # add items to the matrix, extending the grid if needed.
        for i in range(len(column)):
            try:
                self._matrix[i].append(column[i])
            except IndexError:
                self._matrix.append([]*len(column) + [column[i]])

        self._update_max_vectors()

        # update sizes
        self.reset_size()

    def get(self, column, row):
        """
        Gets the content of a cell within the grid.
        If invalid, it raises an IndexError.
        """
        return self._matrix[row][column]

    def set(self, column, row, item):
        """
        Set the content of a cell within the grid,
        substituting existing content.
        """
        item = item or Spacer()
        assert isinstance(item, Viewer)

        self._content.remove(self._matrix[row][column])
        self._matrix[row][column].delete()
        self._matrix[row][column] = item
        self._content.append(item)

        item.set_manager(self._manager)
        item.parent = self
        item.load()
        self.reset_size()

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

    def compute_size(self):
        # calculates the size and the maximum widths and heights of
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
        super(GridContainer, self).delete()
        self._matrix = [[]]


class Wrapper(Container):
    """
    A Viewer that wraps another widget.
    """
    def __init__(self, content, is_expandable=False, anchor=ANCHOR_CENTER, offset=(0, 0)):
        assert isinstance(content, Viewer)
        Container.__init__(self, [content])

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
        return self._content[0]

    @content.setter
    def content(self, content):
        assert isinstance(content, Viewer)
        self.content.delete()

        self._content[0] = content
        self.content.set_manager(self._manager)
        self.content.parent = self
        self.content.load()
        self.reset_size()

    def expand(self, width, height):
        if self.content.is_expandable():
            self.content.expand(width, height)
        self.width = width
        self.height = height

    def is_expandable(self):
        return self.expandable

    def compute_size(self):
        return self.content.width, self.content.height

    def layout(self):
        x, y = GetRelativePoint(self, self.anchor, self.content, self.anchor, self.content_offset)
        self.content.set_position(x, y)
