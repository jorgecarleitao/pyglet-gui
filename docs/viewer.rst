Viewers
=========

This section describes how the viewer API works and how you can use it.

.. currentmodule:: pyglet_gui.core

Managed
----------

.. class:: Managed

    A managed is an abstract class from where all GUI elements derive from.
    Like the name suggests, it is managed by a :class:`~pyglet_gui.core.Manager`. It is attached to
    a manager using

    .. method:: set_manager

        Sets the manager of this class.

    This class exposes important attributes of the manager such as the theme and (manager's) batch.
    It represents the idea that any controller or viewer in
    Pyglet-gui are regulated by a :class:`~pyglet_gui.core.Manager`.

    .. method:: get_batch

        Returns a dictionary of the form {'batch': batch, 'group': group}
        where `group` is a string from the available drawing groups of the manager.

    .. attribute:: theme

        A read-only property that returns its manager's theme.

Rectangle
----------

.. class:: Rectangle

    A geometric rectangle represented by x, y, width and height. It is used for different operations
    on Pyglet-gui.

    .. attribute:: x, y

        The position of the rectangle

    .. attribute:: width, height

        The size of the rectangle

    .. method:: is_inside

        Returns True if point (x,y) lies inside the rectangle

    .. method:: set_position

        Setter for (x, y).


Viewer
----------

.. class:: Viewer

    A viewer, subclass of :class:`Managed` and :class:`Rectangle`, is generic way of displaying
    Pyglet-gui elements in a window.

    Viewers are organized in a tree structure where the manager is always the root.
    A viewer is always a leaf of the tree, and the nodes :class:`~pyglet_gui.containers.Container`.

    It can have graphical elements that have to be defined by subclasses.

    The main idea behind drawing in Pyglet-gui is that the viewer's
    appearance is defined by the path it chooses, defined in :meth:`get_path`.

    .. method:: get_path

        Returns the viewer's path on the theme.

        :meth:`get_path` can return a different path depending on the viewer's state.
        One example is in pyglet-gui's :class:`~pyglet_gui.button.Button`::

            def get_path(self):
                path = ['button']
                if self.is_pressed():
                    path.append('down')
                else:
                    path.append('up')
                return path


    To draw elements, a viewer assigns graphical elements to its manager's batch.
    This is done by calling :meth:`~pyglet_gui.theme.Template.generate` for each of its graphics
    in the method

    .. method:: load_graphics

        Method used to :meth:`~pyglet_gui.theme.Template.generate` graphics this viewer owns. It
        normally calls :meth:`get_theme` to retrieve the specific subset of theme it needs::

            theme = self.theme[self.get_path()]

        followed by calls of the form::

            # _button is a graphic element.
            self._button = theme['image'].generate(color=theme['gui_color'], **self.get_batch('background'))


    Analogously, a viewer has to define the method :meth:`unload_graphics` to deconstruct
    the generated graphics from load.

    .. method:: unload_graphics

        Method used to unload graphics loaded in :meth:`load`.

        Normally implemented as::

            self._button.unload()

    Most of the times, load and unload are called consecutively: when the viewer wants to change its appearance,
    e.g. because it changed its state, it has to unload itself to remove the graphics from the batch,
    and load again (using the new path). Pyglet-gui provides the method :meth:`reload` for that:

    .. method:: reload

        Calls unload followed by load. Used normally in the bottom-up drawing scheme when the element change
        its state (e.g. by an event).

    One important feature of a viewer is that it is not supposed to overlap with other viewers from the same
    manager. This means that is its parent who decides its position. However, in order
    for the parent to decide, it has to know what are the sizes of the children viewers, which are computed
    by the method :meth:`compute_size`:

    .. method:: compute_size

        Computes the size of the viewer and returns the tuple (width, height).

        The size must include all graphics and possible children the viewer has; this is
        the bounding box of the viewer to avoid overlaps.

    When the parent has the size of all its children, it sets the position of the Viewer, :meth:`set_position`:

    .. method:: set_position

        A setter for the position of the viewer. Calls :meth:`layout` afterwards.

    After its own position is set, it needs to re-position its graphics. This is done with the method :meth:`layout`:

    .. method:: layout

        Places graphical elements in the correct positions. Implementation is made on subclasses.

    The glue that defines the functionality of the viewer is the method :meth:`reset_size`, which is worth
    transliterating::

        def reset_size(self, reset_parent=True):
            width, height = self.compute_size()

            # we only reset the parent if we change size
            changed = False
            if self.width != width or self.height != height:
                self.width, self.height = width, height
                changed = True
            self.layout()
            # we only reset parent if the parent exists and
            # the flag to reset it is set.
            if changed and reset_parent:
                self.parent.reset_size(reset_parent)

    .. method:: reset_size

        The case reset_parent=False updates the viewer size and lays out the graphics. This call
        is a top-down draw: it is called when it was the parent's initiative to reset_size of the viewer.

        The reset_parent=True does the same and, if the size changes, it calls the parent's reset_size. This call
        is the bottom-up draw: the child decided to start a reset_size.

        This call means that the parent will re-calculate its own size, and calls reset_size of all children, with flag
        reset_parent=False (see :meth:`pyglet_gui.container.Container.reset_size`). This ensures that all its
        children are affected by the change in size of one of them.
        This call is further propagated to parent's parent in order to accommodate the size changes.

    Finally, the viewer implements a :meth:`delete`, used for deleting the element

    .. method:: delete

        Used to delete the viewer: :meth:`unload` all its graphics, and undo all things done by initialization.
