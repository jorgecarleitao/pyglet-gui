Viewers
=========

This section describes how the viewer API works and how you can use it.

.. currentmodule:: pyglet_gui.core

Managed
----------

.. class:: Managed

    A managed is an abstract class from where all GUI elements derive from.
    Like the name suggests, it is managed by a :class:`~pyglet_gui.manager.Manager`. It is attached to
    a manager using

    .. method:: set_manager

        Sets the manager of this class.

    This class exposes important attributes of the manager such as the theme and (manager's) batch.
    It represents the idea that any controller or viewer in Pyglet-gui are managed by
    a :class:`~pyglet_gui.manager.Manager`.

    .. method:: get_batch

        Returns a dictionary of the form {'batch': batch, 'group': group}
        where `group` is a string from the available drawing :attr:`groups <pyglet_gui.manager.ViewerManager.group>` of
        the manager.

    .. attribute:: theme

        A read-only property that returns its manager's theme.

Rectangle
----------

.. class:: Rectangle

    A geometric rectangle represented by x, y, width and height. It is used for different operations
    in Pyglet-gui.

    .. attribute:: x, y

        The position of the rectangle

    .. attribute:: width, height

        The size of the rectangle

    .. method:: is_inside

        :param x:
        :param y:

        Returns True if point (x,y) lies inside the rectangle

    .. method:: set_position

        :param x:
        :param y:

        Setter for (x, y).


Viewer
----------

.. class:: Viewer

    A viewer, subclass of :class:`Managed` and :class:`Rectangle`, is generic way of displaying
    Pyglet-gui elements in a window.

    Viewers are organized in a tree structure where the manager is always the root,
    the nodes are :class:`Containers <pyglet_gui.containers.Container>`, and viewers are leafs.

    Viewers can have graphical elements that have to be defined by subclasses and are loaded by :meth:`load_graphics`.

    In Pyglet-gui, the viewer's appearance is defined by the path it chooses from the Theme,
    defined in :meth:`get_path`.

    .. method:: get_path

        Returns the viewer's path on the theme.

        :meth:`get_path` can return a different path depending on the viewer's state,
        for example, in pyglet-gui's :class:`~pyglet_gui.button.Button`::

            def get_path(self):
                path = ['button']
                if self.is_pressed():
                    path.append('down')
                else:
                    path.append('up')
                return path

        leads to a different appearance depending on whether the button is pressed or not.

    To draw elements, a viewer assigns graphical elements to its manager's batch using :meth:`~pyglet_gui.core.Managed.get_batch`
    This is done by calling :meth:`~pyglet_gui.theme.Template.generate` for each of its graphics
    in the method

    .. method:: load_graphics

        Method used to :meth:`~pyglet_gui.theme.Template.generate` graphics this viewer owns. It
        normally calls :meth:`get_path` to retrieve the specific subset of theme it needs::

            theme = self.theme[self.get_path()]

        followed by calls of the form::

            self._button = theme['image'].generate(color=theme['gui_color'], **self.get_batch('background'))
            # _button is now a loaded graphic element.


    Analogously, a viewer has to define the method :meth:`unload_graphics` to deconstruct
    the generated graphics from load.

    .. method:: unload_graphics

        Method used to unload graphics loaded in :meth:`load_graphics`.

        Example::

            # _button is a loaded graphic element.
            self._button.unload()

    Most of the times, load and unload are called consecutively: when the viewer wants to change its appearance,
    e.g. because it changed its state, it has to unload itself to remove the graphics from the batch,
    and load them again using the new path. Pyglet-gui provides the method :meth:`reload` for that:

    .. method:: reload

        Calls unload followed by load. Used in the bottom-up drawing scheme when the element change
        its state (e.g. by an event).

        This is used to update the graphics whenever the Viewer changed state.

    One important feature of a viewer is that it is not supposed to overlap with other viewers from the same
    GUI. This means that is its parent who decides its position. The method :meth:`compute_size`
    returns the computed size of the viewer from the Graphics it has.

    .. method:: compute_size

        Computes the size of the viewer and returns the tuple (width, height). Implementation is made by subclasses.

        The size must include all graphics and possible children the viewer has; this is
        the bounding box of the viewer to avoid overlaps.

        The default implementation returns (self.width, self.height).

    When the parent has the size of all its children, it sets the position of the Viewer, using :meth:`set_position`:

    .. method:: set_position

        :param x:
        :param y:

        A setter for the position of the viewer. Calls :meth:`layout` after to ensure the graphics are also
        set.

    .. method:: layout

        Places graphical elements in the correct positions in relation to the viewer's position.

        Default implementations does nothing.

    What defines the functionality of the viewer is the method :meth:`reset_size`, which is worth
    transliterating::

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

    .. method:: reset_size

        :param reset_parent: A boolean, see below.

        The case `reset_parent = False` updates the viewer size and :meth:`layout` if the size changed. This call
        is what we call a top-down draw: it is called when it was the parent's initiative to reset_size of the viewer.

        The `reset_parent = True` does the same but, if the size changes, it also calls the parent's reset_size. This call
        is the bottom-up draw: the child decided to trigger a reset_size.

        In the button-up, the parent will re-calculate its own size, and calls reset_size of all children, with
        `reset_parent = False`. This ensures that all its children are affected by the size change of one of them.

        This call can be further propagated to the parent's parent in order to
        accommodate the size changes of all elements.

        In situations where an event was triggered (e.g. by a :class:`Controller`),
        the bottom-up is the correct way, thus
        `reset_size()` should be called after :meth:`reload()`. For example, Pyglet-gui's
        :class:`pyglet_gui.button.Button` uses::

            def change_state(self):
                self._is_pressed = not self._is_pressed
                self.reload()
                self.reset_size()

    Finally, the viewer implements a :meth:`delete`, used for deleting the element

    .. method:: delete

        Used to delete the viewer: calls :meth:`unload_graphics` and undo initialization.
