class Managed(object):
    def __init__(self):
        self._manager = None

    def set_manager(self, manager):
        self._manager = manager

    def has_manager(self):
        return self._manager is not None

    def get_batch(self, group):
        return {'batch': self._manager.batch, 'group': self._manager.group[group]}

    @property
    def theme(self):
        assert self._manager is not None
        return self._manager.theme

    def delete(self):
        self._manager = None


class Rectangle(object):
    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self.width = width
        self.height = height

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def is_inside(self, x, y):
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


class Viewer(Rectangle, Managed):
    def __init__(self, width=0, height=0):
        super(Managed, self).__init__()
        self._parent = None
        self._is_loaded = False

        Rectangle.__init__(self, 0, 0, width, height)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, widget):
        self._parent = widget

    @property
    def is_loaded(self):
        return self._is_loaded

    def is_expandable(self):
        return False

    def set_position(self, x, y):
        super(Viewer, self).set_position(x, y)
        self.layout()

    def get_path(self):
        raise NotImplementedError

    def load(self):
        assert not self._is_loaded
        self._is_loaded = True
        self.load_graphics()

    def unload(self):
        assert self._is_loaded
        self._is_loaded = False
        self.unload_graphics()

    def reload(self):
        self.unload()
        self.load()

    def load_graphics(self):
        pass

    def unload_graphics(self):
        pass

    def layout(self):
        pass

    def compute_size(self):
        return self.width, self.height

    def reset_size(self, reset_parent=True):
        width, height = self.compute_size()

        # if out size changes
        if self.width != width or self.height != height:
            self.width, self.height = width, height

            # This will eventually call our layout
            if reset_parent:
                self.parent.reset_size(reset_parent)
        # else, the parent is never affected and thus we layout.
        else:
            self.layout()

    def delete(self):
        if self.is_loaded:
            self.unload()
        self.parent = None
        Managed.delete(self)


class Controller(Managed):
    def __init__(self):
        Managed.__init__(self)

    def set_manager(self, manager):
        Managed.set_manager(self, manager)
        manager.add_controller(self)

    def delete(self):
        self._manager.remove_controller(self)
        super(Controller, self).delete()
