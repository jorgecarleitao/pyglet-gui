Containers
===============

.. currentmodule:: pyglet_gui.containers


Container
----------

.. class:: Container

    A container is the base class of all containers in Pyglet-gui and is used to group
    viewers and position them in specific ways.

    In the :class:`~pyglet_gui.core.Viewer` API, a container is a node in the tree of viewers.

    A container is characterized by a set of viewers and how they are positioned in the container's bounding box.

    While viewers only have to load graphics, a container has to load both its graphics and its content.
    Thus, the container provides two aditional methods for those:

    .. method:: load_content

        Loads each element inside its content

    .. method:: unload_content

        Unloads each element inside its content

    Notice that both these methods are correctly called during a reload.
    The getters and setters of content are:

    .. attribute:: content

        A read-only property returning the content of the container.

    .. method:: add

        Adds the viewer to the container's content.

    .. method:: remove

        Removes the viewer from the container's content.
