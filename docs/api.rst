API
===========

This document gives a conceptual overview of how Pyglet-gui works.

Pyglet-gui follows a :class:`pyglet_gui.core.Viewer`-:class:`pyglet_gui.core.Controller` pattern.
It uses rectangular viewers - :class:`Widgets <pyglet_gui.widgets.Widget>` - for appearance,
and controllers, for events.
For instance, a (rectangular) button is a mixing of a Widget with a Controller.

Drawing viewers
-----------------

In Pyglet-gui, the widgets are organized in a tree: every widget has a parent
and can have children. The root of the tree is a :class:`~pyglet_gui.dialog.Dialog`, a special
widget with no parent that defines a GUI within a pyglet window. This structure is essentially used to draw elements and
Pyglet-gui provides two ways to draw a GUI: top-down and bottom-up.

Top-down is a recursion in the tree used when :class:`~pyglet_gui.dialog.Dialog` wants
to draw itself (e.g. initialization):
the dialog :meth:`loads <pyglet_gui.core.Viewer.load>` the children's graphics
(which is propagated to the children of the children).
With the graphics loaded, its size is computed by computing the size
of each child (:meth:`~pyglet_gui.core.Viewer.compute_size`), again propagated.
Finally, it sets the positions of the children and his position in the window (:meth:`~pyglet_gui.core.Viewer.set_position`).
This process is wrapped in the functions :meth:`~pyglet_gui.core.Viewer.reload` and :meth:`~pyglet_gui.core.Viewer.reset_size`.

The bottom-up approach is used when a single Widget wants to be re-drawn, e.g. when a button was pressed.
First, it :meth:`~pyglet_gui.core.Viewer.unload` the
graphics and :meth:`~pyglet_gui.core.Viewer.load` them with the new state in consideration;
second, it re-computes its size (:meth:`~pyglet_gui.core.Viewer.reset_size`).
If the size changed, it asks a reload of the parent widget,
which in turn re-computes the parent size and so one and so forth.
This means that when a widget changes its appearance, the dialog is
re-laid out only if the change was propagated up to it.

Controllers
-------------

The other special feature of the dialog is that it handles all pyglet events
and sends them to the controllers it contains. So, while widgets are organized as a tree,
the controllers are organized in a simple list: each controller registers itself in the
dialog and the dialog has access to all of them.

The dialog is fully responsible for the user behaviour in itself.
It is the one who assigns which controllers receive mouse hovering, keyboard strokes etc.

Graphical elements
-----------------

Each widget can have graphical elements (e.g. textures, text).
Pyglet-gui has a :doc:`graphics API <theme_api>` for handling those, Pyglet-gui
abstracts the idea of images: it uses a high-level interface
on which you build a :class:`pyglet_gui.theme.Theme` (a JSON file with paths to files and colors)
and widgets select the part of the theme
they need by selecting the path in the dictionary (:meth:`~pyglet_gui.core.Viewer.get_path`).

Conceptually, Pyglet-gui Theme follows the factory pattern: it has a class "template" that is instantiated
when the theme is loaded, and each template has a method to generate the actual graphics
by assigning vertices to the drawing batch.
Graphics generation is called from :meth:`pyglet_gui.core.Viewer.load`.

Examples
----------

In the source code you find concrete examples of how all this works in pratice: all user interfaces
in Pyglet-gui are subcasses of :class:`~pyglet_gui.core.Controller` and/or :class:`~pyglet_gui.widgets.Widget`
that implement custom :meth:`~pyglet_gui.core.Viewer.get_path`, :meth:`~pyglet_gui.core.Viewer.load`,
:meth:`~pyglet_gui.core.Viewer.unload`, :meth:`~pyglet_gui.core.Viewer.layout`
and :meth:`~pyglet_gui.core.Viewer.compute_size`.

In the directory "examples", you can find examples of how to instantiate GUIs and how to extend the existing
elements.


Extending functionality
===========================

Pyglet-gui already has some end-user interfaces such as sliders and buttons, but they are designed to be extended
to the developer's need.

To extend a :class:`~pyglet_gui.widgets.Widget` (or a subclass of), you should worry about

1. :meth:`~pyglet_gui.widgets.Widget.get_path`

    Used to select the path on the theme for its graphics.

2. :meth:`~pyglet_gui.widgets.Widget.load`, :meth:`~pyglet_gui.widgets.Widget.unload`

    Used to load and unload graphical elements.

3. :meth:`~pyglet_gui.widgets.Widget.layout`

    Used to layout the graphics in the correct place.

4. :meth:`~pyglet_gui.widgets.Widget.compute_size`

    Used to compute the size of the Widget when all graphics are already loaded.


To extend a :class:`~pyglet_gui.core.Controller`, you should worry about:

1. on_* (e.g. on_press(...))

    They are used to receive events that are passed.


Existing user interfaces
===========================

Viewers:
    * Graphics: a widget with a graphic element from the theme.
    * Spacer: an empty widget for filling space in containers
    * Label: a widget that holds text.

Controllers:
    * TwoStateController: a controller with two states.
    * ContinuousStateController: a controller with a float value state.
    * Slider: a ContinuousStateController with continuous or discrete states and 3 graphic elements: a bar, a knob and markers.

Containers:
    * Vertical: widgets inside are arranged vertically.
    * Horizontal: widgets inside are arranged horizontally.
    * Grid: widgets inside are arranged in a grid (you provide a matrix of them).
    * Free: widgets inside are freely arranged.
    * Frame: a wrapper that adds a graphical frame around a widget.
    * Document: a widget that holds pyglet documents (with scrollbar).
    * Scrollable: a wrapper with scrollable content.

End-user controllers:
    * Button: a On/Off button with a label and graphics placed on top off each other.
    * Checkbox: a Button where the label is placed next to the graphics (and graphics is a checkbox like button).
    * OneTimeButton: a Button which turns off when is released.
    * HorizontalSlider: an implementation of an Horizontal Slider.
    * TextInput: a box for writing text.
