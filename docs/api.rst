Overview of the API
===================

This document gives a conceptual overview of how Pyglet-gui works.

Pyglet-gui uses :class:`Viewers <pyglet_gui.core.Viewer>` for static appearance
and :class:`Controllers <pyglet_gui.core.Controller>` for dynamic events.
For instance, a button is a mixing of a Viewer (for draw) with a Controller (for user actions).

.. image:: management.png
    :scale: 100%

:class:`~pyglet_gui.manager.Manager` constitutes a GUI in a Pyglet-gui,
managing :class:`Controllers <pyglet_gui.core.Controller>` and :class:`Viewers <pyglet_gui.core.Viewer>`.

Viewers
^^^^^^^^^^^

In Pyglet-gui, the viewers are organized in a tree: every viewer has a
parent :class:`~pyglet_gui.containers.Container` (a subclass of Viewer with children).
The root of the tree is a :class:`~pyglet_gui.manager.ViewerManager`, a special
container without parent.

.. image:: tree.png
    :scale: 100%

This structure is essentially used to draw elements. Pyglet-gui provides two orthogonal ways
to update elements in the tree, the top-down and bottom-up,
that minimize the number of operations in the drawing Batch.

* Top-down when a container wants
to draw itself (e.g. in the initialization of the :class:`~pyglet_gui.manager.Manager`).

* Bottom-up when a single Viewer wants to be re-drawn, for instance
when a :class:`Controller's <pyglet_gui.core.Controller>` changed the viewer's appearance.

Graphical elements
^^^^^^^^^^^^^^^^^^^^

Pyglet-gui has a graphics API for handling vertex list:
you define a :class:`pyglet_gui.theme.Theme` in a JSON file or on a nested dictionary, and viewers select
the part they need from the theme using :meth:`~pyglet_gui.core.Viewer.get_path`.

Controllers
^^^^^^^^^^^^^^

The :class:`~pyglet_gui.manager.ControllerManager` is responsible for handling all events in the GUI
and calling the respective :class:`Controllers' <pyglet_gui.core.Controller>` handlers.

.. image:: controllers.png
    :scale: 100%

While viewers are organized in a tree, the controllers are organized in a simple list:
each controller registers itself in the manager and the manager has access to all of them.

Examples
^^^^^^^^^^^^

In the directory "examples" you can find examples of how to instantiate GUIs and how to extend the existing
elements.

In the source code you can find more examples since all Pyglet-gui
user interfaces are subclasses of :class:`~pyglet_gui.core.Controller`, :class:`~pyglet_gui.core.Viewer`, or
are a mixin of both that implement custom methods:

* :meth:`~pyglet_gui.core.Viewer.get_path`: Used to select the path on the theme for its graphics;
* :meth:`~pyglet_gui.core.Viewer.load_graphics` and :meth:`~pyglet_gui.core.Viewer.unload_graphics`: Used to load and unload graphical elements from the theme;
* :meth:`~pyglet_gui.core.Viewer.layout`: Used to position the graphical elements in the correct place;
* :meth:`~pyglet_gui.core.Viewer.compute_size`: Used to compute the size of the Viewer when all graphics are already loaded;
* `on_*`: used to handle events.

Existing user interfaces
^^^^^^^^^^^^^^^^^^^^^^^^

Viewers:
    * Graphics: a viewer with a graphic element from the theme.
    * Spacer: an empty viewer for filling space in containers.
    * Label: a viewer that holds text.
    * Document: a viewer that holds Pyglet documents (optionally with a scrollbar).

Controllers:
    * :class:`~pyglet_gui.controllers.TwoStateController`: a controller with two states.
    * :class:`~pyglet_gui.controllers.ContinuousStateController`: a controller with a float value state.

Containers:
    * Vertical: widgets inside are arranged vertically.
    * Horizontal: widgets inside are arranged horizontally.
    * Grid: widgets inside are arranged in a grid (you provide a matrix of them).
    * Frame: a wrapper that adds a graphical frame around a viewer.
    * Scrollable: a wrapper with scrollable content.

End-user controllers:
    * :class:`~pyglet_gui.buttons.Button`: a On/Off button with a label and graphics placed on top off each other.
    * Checkbox: a Button where the label is placed next to the graphics (and graphics is a checkbox like button).
    * OneTimeButton: a Button which turns off when is released.
    * Slider: a ContinuousStateController with continuous or discrete states and 3 graphic elements: a bar, a knob and markers.
    * HorizontalSlider: an implementation of an Horizontal Slider.
    * TextInput: a box for writing text.
