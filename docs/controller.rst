Controllers
===============

.. currentmodule:: pyglet_gui.core


Controller
----------

.. class:: Controller

    A controller is an abstract class that represents something that can be controlled.

    The main functionality of a controller is to attach itself
    to a list of controllers of the :class:~`pyglet_gui.core.Manager`.

    A controller can receive an event (e.g. "on_press") from the manager if it has
    that method implemented (i.e. the manager uses :py:meth:`hasattr` to decide if sends the event to the controller or not).

    When mixing a Controller with a Viewer, the controller has to be the first parent-class
    or you have to write a custom :meth:`~Managed.set_manager`, since it uses this method to subscribe to the manager's list
    of controllers.

    Subclasses of a controller receive events by having on_* methods defined.

    To receive mouse events, the controller has to define the method :meth:`hit_test(x, y)`, which returns True
    if the point (x, y) is inside the controller and False otherwise.


Two state controller
----------------------

.. currentmodule:: pyglet_gui.controllers

.. class:: TwoStateController

    A two state controller is a :class:`Controller` with a two state characterized by the property `is_pressed`.

Continuous state controller
----------------------

.. class:: ContinuousStateController

    A continuous state controller has a state in a continuous interval [min_value, max_value],
    characterized by the property `value`.
