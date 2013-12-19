Controllers
===============

.. currentmodule:: pyglet_gui.core


Controller
----------

.. class:: Controller

    A controller is an abstract class that represents something that can be controlled by the user.

    Controllers are organized in a flat list inside the :class:~`pyglet_gui.core.Manager`
    without stacking because events are normally assigned to specific controllers where the user is currently interacting.

    A controller can receive a event (e.g. "on_press") from the manager when it has
    that method implemented (i.e. the manager uses :py:meth:`hasattr` to decide if sends the event to the controller or not).

    Since the manager is responsible for calling the controllers methods, when a controller is
    assigned to a manager, it subscribes itself to the list of the manager's controllers, overriding the method
    :meth:`~Managed.set_manager`. If you mix a Controller with
    a Viewer, the controller has to be the first parent-class or you have to write a custom :meth:`~Managed.set_manager`
    to subscribe to the manager.

    Subclasses of a controller can receive events by having on_* methods defined.

    To receive mouse events, the subclass has to define the method :meth:`hit_test(x, y)`, which returns True
    if the point (x, y) is inside the controller and False otherwise.


Two state controller
----------------------

.. currentmodule:: pyglet_gui.controllers

.. class:: TwoStateController

   A two state controller is a :class:`Controller` with a two state characterized by the property `is_pressed`.
