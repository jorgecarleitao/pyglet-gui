Theme
=======

.. currentmodule:: pyglet_gui.theme

Pyglet-gui Theme API defines a systematic approach for mapping a set of resources (e.g. image.png)
and attributes (e.g. color, padding) to lists of vertices and vertex attributes.

The API works as follows:

* The user defines a set of attributes and sources of static resources in a JSON file;
* A set of :class:`Parsers <parsers.Parser>` translate that to :class:`Templates <templates.Template>`;
* A :class:`theme.Theme`, a nested dictionary, holds those templates with a unique identifier (a path on the nested dictionary)
* A :class:`theme.Theme` is passed to the :class:`pyglet_gui.manager.ViewerManager`,
and :class:`Viewers <pyglet_gui.core.Viewer>` load concrete graphical elements, :class:`GraphicElement`.

This document explains how this API works in detail. It starts by explaining
Graphic elements, goes to Templates, Parsers, Theme, and ends in the JSON file.


Graphic elements
^^^^^^^^^^^^^^^^^^^^

.. class:: elements.GraphicElement

    A graphical element is a subclass of :class:`pyglet_gui.core.Rectangle` and an abstract class that
    represents something with a set of vertices and a set of rules
    to assign a set of attributes (e.g. color, texture coordinate) to the vertices.

    A GraphicalElement is normally instantiated by a :class:`templates.Template` because it does not own
    static resources. The initialization of this element needs a batch and a group to assign its
    vertices to a group in the batch.

    A graphical element provides three methods for accessing its size:

    .. method:: get_content_region

        Returns the tuple (x, y, width, height) with its region.

    .. method:: get_content_size

        Returns the tuple (width, height) with the size this element.

    .. method:: get_needed_size

        Returns the tuple (width, height) with the size required for this element.

    After the element is initialized, its size and position can be updated using :meth:`update`:

    .. method:: update

        Updates the position and size of the graphics, updating its vertex list in the Batch.

    When it is no longer needed, it can be destroyed using :meth:`unload`:

    .. method:: unload

        Removes the vertex list from the Batch.

Pyglet-gui provides two concrete implementations of a Graphical element:

.. class:: elements.TextureGraphicElement

    A subclass of :class:`GraphicElement` representing a rectangle of vertices with a texture.


.. class:: elements.FrameTextureGraphicElement

    A subclass of :class:`GraphicElement` representing 9 rectangles, as represented in the figure

    .. figure:: frame_texture_source.svg
       :scale: 100%
       :align: center
       :alt: Diagram of how frame texture works.

        How the :class:`FrameTextureGraphicElement` maps an image into a rectangle. Notice that if the rectangle
        changes size, each of the 9 rectangles will increase independently, and the image will be stretched on each one
        independently.

    The :meth:`elements.GraphicElement.get_content_size` is overridden to return the size of the inner rectangle.

Templates
^^^^^^^^^^^^

For generating graphical elements, Pyglet-gui uses the concept of template.

.. class:: templates.Template

    An abstract class that provides the method :meth:`generate`
    to return a new instance of a :class:`elements.GraphicalElement` (or subclass of).

    A template is normally instantiated by a Parser, when the Theme is being loaded.

    .. method:: generate

        Returns a new instance of a :class:`elements.GraphicalElement`. It is an abstract method.

Pyglet-gui provides two concrete implementations of a templates:

.. class:: templates.TextureTemplate

    A :class:`templates.Template` that generates a :class:`elements.TextureGraphicElement`.


.. class:: templates.FrameTextureTemplate

    A :class:`templates.TextureTemplate` that generates a :class:`elements.FrameTextureGraphicElement`.
