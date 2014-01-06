Containers
===============

.. currentmodule:: pyglet_gui.containers


Container
----------

.. class:: Container

    A :class:`~pyglet_gui.core.Viewer` that contain other viewers. This is an abstract and base class of
    all containers in Pyglet-gui and is used to group viewers and position them in specific ways.

    In the :class:`~pyglet_gui.core.Viewer` API, a container is a node in the tree of viewers.

    While viewers only have to load graphics, a container has to load both its graphics and its content.
    Thus, the container provides two aditional methods:

    .. method:: load_content

        Loads all viewers in the container

    .. method:: unload_content

        Unloads all viewers in the container

    Both these methods are already correctly called during a :meth:`~pyglet_gui.core.Viewer.reload`.

    The getters and setters of content are:

    .. attribute:: content

        A read-only property returning the content of the container.

    .. method:: add(viewer)

        Adds the viewer to the container's content.

    .. method:: remove(viewer)

        Removes the viewer from the container's content.

Other containers
-----------------

.. class:: Wrapper

    .. _`decorator pattern`: http://en.wikipedia.org/wiki/Decorator_pattern

    A wrapper is a container that contains one and only one Viewer. It follows the `decorator pattern`_.

    It does not have any graphical appearance and is used
    by Pyglet-gui for creating more interesting elements such
    as the :class:`~pyglet_gui.manager.ViewerManager`.
