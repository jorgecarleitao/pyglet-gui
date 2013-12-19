Button
===============

.. currentmodule:: pyglet_gui.button

Pyglet-gui ships a standard button that you can use, and two variations of it.
The important fact is that a Button is a mixing of:

* :class:`~pyglet_gui.controller.TwoStateController`
* :class:`~pyglet_gui.core.Viewer`

because it is a controllable viewer with two states ("is pressed" and "is not pressed").

.. class:: Button

    A two state and clickable :class:`~pyglet_gui.core.Viewer` represented as a
    label and graphics drawn on top of each other.

    :param label: A string written in the button graphics.
    :param is_pressed: True if the button starts pressed
    :param on_press: A callback function of one argument called when the button is pressed.

    Attributes:

    .. attribute:: label

        The label of the button (a string).

    Accepted events:

    .. method:: on_mouse_press

        Switches the state of the button. It is an event handler.

    Default paths in the theme:

    .. attribute:: [button, down], [button, up]

.. class:: OneTimeButton

    A :class:`Button` that changes back to its original state when the mouse is released.

    :param label: A string written in the button graphics.
    :param on_release: A callback function of one argument called when the button is released.

    Accepted events:

    .. method:: on_mouse_release

    Switches the state back and calls the callback if the mouse was released inside the button.

.. class:: Checkbox

     A button drawn as a checkbox icon with the label on the side.

    :param label: A string written in the button graphics.
    :param is_pressed: True if the button starts pressed
    :param on_press: A callback function of one argument called when the button is pressed.
    :param align: Whether the label is left or right of the checkbox.
    :param padding: The distance from the label to the checkbox.

    Path in the theme:

    .. attribute:: ['checkbox', 'checked'], ['checkbox', 'unchecked']
