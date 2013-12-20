Controllers
===============

.. currentmodule:: pyglet_gui.core


A viewer, by itself, cannot be interacted by events; it is a static element. On the other hand,
a :class:`~pyglet_gui.core.Controller` is a dynamic element that does not have a geometric representation
and is not able to draw itself on the screen.

To provide functionality to a viewer, or to provide drawing features to a controller, Pyglet-gui mixes both.

This section introduces the API for controllers.


Controller
----------

.. class:: Controller

    A controller is an abstract class that represents something that can be controlled.

    The main functionality of a controller is to attach itself
    to a list of controllers of the :class:`~pyglet_gui.manager.ControllerManager`.

    .. method:: set_manager

        Sets its manager and calls::

            manager.add_controller(self)

        When mixing a Controller with a Viewer, the controller has to be the first parent-class
        or you have to write a custom :meth:`~pyglet_gui.core.Managed.set_manager`.

    This way, the :class:`~pyglet_gui.manager.ControllerManager` can dispatch calls when it handles events from the Pyglet's window.
    To a controller receive events (e.g. "on_press"), it has to have the method
    implemented (i.e. the manager uses :py:meth:`hasattr` to decide if it sends the event to the
    controller or not). The signature of the method must be the same same as of Pyglet (or, if you want, the one
    :class:`~pyglet_gui.manager.ControllerManager` calls).

    To receive mouse events, the controller has to define :meth:`hit_test(x, y)`, which returns True
    if the point (x, y) is inside the controller and False otherwise.


Two state controller
----------------------

.. currentmodule:: pyglet_gui.controllers

The simplest example of a controller is one that flips between two states.
Pyglet-gui provides a simple abstraction of such behavior in the :class:`~pyglet_gui.controllers.TwoStateController`.

.. class:: TwoStateController

    A :class:`Controller` with two possible values characterized by the read-only property :attr:`is_pressed`.
    This controller accepts the following arguments:

    :param on_press: An optional callback function of one boolean argument that is called when the controller changes state.
    :param is_pressed: An optional boolean for deciding the state on initialization.

    .. attribute:: is_pressed

        True if in one state, False in the other.

    This controller has the method

    .. method:: change_state

        Flips the state of the controller and calls on_press if it is defined.


Continuous state controller
----------------------

Another example of a useful controller is a controller with a continuous set of values within an interval.
Pyglet-gui provides a simple abstraction of such behavior in the :class:`~pyglet_gui.controllers.ContinuousStateController`.

.. class:: ContinuousStateController

    A :class:`Controller` with a state in a continuous interval [min_value, max_value]
    characterized by the read-only property :attr:`value`.

    :param value: The initial value. Default to 0
    :param min_value: Default to 0.0
    :param max_value: Default to 1.0
    :param on_set: An optional callback function of one float argument that is called when the controller changes value.

    .. attribute:: value

        The value of the controller. A read-only property.

    This controller has the method

    .. method:: set_value

        The setter for the value. Calls on_set if it is defined. The value must belong to [min_value, max_value].

Options and selectors
-----------------------

One useful GUI less trivial example of a controller is selector: a menu with a set of options, and the user
can choose one and only one.
Pyglet-gui provides an abstraction of such behavior in the :class:`~pyglet_gui.controllers.Option` and
:class:`~pyglet_gui.controllers.Selector`.

.. class:: Option

    A :class:`Controller` with a name and a parent selector. The name is used as an id in the parent selector.
    This controller is initialized by a name and a parent:

    :param name: Mandatory string
    :param parent: Mandatory :class:`~Selector`.

    and has one method

    .. method:: select

        Makes him the current selection of the parent.

.. class:: Selector

    An abstract class with a set of options labeled by a string. The arguments are

    :param options: Mandatory list of strings identifying the options.
    :param labels: Optional list of strings with the same length of options labeling the options.
    :param on_select: Optional callback function that will receive one argument, the selected option name.
    :param selected: Optional string (belonging to "options" setting a initially-selected item.

    This class has two methods:

    .. method:: select

        Selects the option name and, if defined, calls on_select.

    .. method:: deselect

        Deselects the current selected option, if any is selected.
