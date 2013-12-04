API
===========

This document gives an overview of how Pyglet-gui works.

Pyglet-gui follows a :class:`pyglet_gui.core.Viewer`-:class:`pyglet_gui.core.Controller` pattern.
Most viewers are :class:`Widgets <pyglet_gui.widgets.Widget>`,
rectangles in space that can be drawn, and all controllers are
:class:`Controllers <pyglet_gui.core.Controller>` that can receive events.
For instance, a button in pyglet-gui is a subclass of both a Widget and a Controller.

In Pyglet-gui, every widget has to be placed inside a :class:`~pyglet_gui.dialog.Dialog`.
A dialog is just a widget that contains other widgets (and controllers).
Its key functionality is that it handles all events pyglet dispatches,
and them sends these events to the controllers it contains.

Each widget can have graphical elements (e.g. textures).
Pyglet-gui has a :doc:`graphics API <theme_api>` for handling graphics,
and abstracts the idea of images and textures: it uses a high-level interface
on which you build a :class:`pyglet_gui.theme.Theme`, and widgets select the part of
the theme they need using :meth:`~pyglet_gui.widgets.Widget.get_path`.

Drawing viewers
-----------------

Pyglet-gui follows the event pattern of Pyglet: viewers and controllers only change state
by events.

Pyglet-gui provides two ways to draw the GUI: top-down and bottom-up. Top-down
is used when :class:`~pyglet_gui.dialog.Dialog` wants to draw itself: first, it loads all
the graphics (:meth:`~pyglet_gui.core.Viewer.reload`), sets their sizes
and sets their positions (:meth:`~pyglet_gui.core.Viewer.reset_size`).

Bottom-up uses the inverse approach: when a Widget was affected by an event, it :meth:`~pyglet_gui.core.Viewer.reload`
its graphics and re-computes its size (:meth:`~pyglet_gui.core.Viewer.reset_size`).
If the size changed, it asks a reload of its parent widget, which in turn re-computes its size and so one and so forth.
This means that when a widget changes its appearance, its Dialog is only reloaded if the change caused a major
change on the dialog layout.

Using controllers
---------------------

A :class:`~pyglet_gui.dialog.Dialog` is responsible for handling all pyglet mouse and keyboard events inside itself
and for sending them to its controllers.
When a controller is added to a dialog, it is automatically added to a dialog.
A Dialog only sends events to owned controllers, and only to controllers that are capable of handling those events.

When a control handles an event successfully, normally it changes its state in some way. This means
that the graphics of the viewer have to be reloaded.
To re-load the graphics, use :meth:`~pyglet_gui.core.Viewer.reload`; to re-compute its size and re-layout,
use :meth:`~pyglet_gui.core.Viewer.reset_size` (typically called in this order).

By peaking the source code, you can find concrete examples of how this works: all user interfaces
shipped with Pyglet-gui are subcasses of :class:`~pyglet_gui.core.Controller` and/or :class:`~pyglet_gui.widgets.Widget`
that implement custom :meth:`~pyglet_gui.core.Viewer.get_path`, :meth:`~pyglet_gui.core.Viewer.load`,
:meth:`~pyglet_gui.core.Viewer.unload`, :meth:`~pyglet_gui.core.Viewer.layout`
and :meth:`~pyglet_gui.core.Viewer.compute_size`.


Mixins
=========

Pyglet-gui uses mixins to extend functionality. E.g. every end-user user interface is a mixing of a
:class:`~pyglet_gui.core.Controller` with a :class:`~pyglet_gui.core.Viewer`, both deriving from the
base of Pyglet-gui the :class:`~pyglet_gui.core.Managed`.

Extending functionality
===========================

Pyglet-gui already ships end-user interfaces such as sliders and buttons, but they are designed to be extended
to the developer's need.

To extend a :class:`~pyglet_gui.widgets.Widget` (or a subclass of), you should worry about

1. :meth:`~pyglet_gui.widgets.Widget.get_path`

    Used to select the path on the theme for its graphics.

2. :meth:`~pyglet_gui.widgets.Widget.load`, :meth:`~pyglet_gui.widgets.Widget.unload`

    Used to load and unload graphics.

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
    * Graphics: a widget with a graphic from theme.
    * Spacer: an empty widget for filling space in containers
    * Label: a widget that holds a text.

Controllers:
    * TwoStateController: a controller with two states.
    * ContinuousStateController: a controller with a float value state.
    * Slider: a ContinuousStateController with continuous or discrete states with 3 graphic elements: a bar, a knob and markers.

Containers:
    * Vertical: widgets inside are arranged vertically.
    * Horizontal: widgets inside are arranged horizontally.
    * Grid: widgets inside are arranged in a grid (you provide a matrix of them).
    * Free: widgets inside are freely arranged.
    * Frame: a wrapper that adds a graphical frame around a widget.
    * Document: a widget that holds pyglet documents (with scroll).
    * Scrollable: a wrapper with scrollable content.

End-user controllers:
    * Button: a On/Off button with a label and graphics placed on top off each other.
    * Checkbox: a Button where the label is placed next to the graphics (and graphics is a checkbox like button).
    * OneTimeButton: a Button which turns off when is released.
    * HorizontalSlider: an implementation of an Horizontal Slider.
    * TextInput: a box for writing input.
