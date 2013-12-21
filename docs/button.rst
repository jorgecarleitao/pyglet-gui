Button
===============

.. currentmodule:: pyglet_gui.buttons

Pyglet-gui ships a standard button and two variations of it. A Button is a mixing of:

* :class:`~pyglet_gui.controller.TwoStateController`
* :class:`~pyglet_gui.core.Viewer`

because it is a controllable viewer with two states ("is pressed" and "is not pressed").

.. class:: Button

    A :class:`~pyglet_gui.controller.TwoStateController` and :class:`~pyglet_gui.core.Viewer`
    represented as a label and texture drawn on top of each other.

    :param label: The string written in the button.
    :param is_pressed: True if the button starts pressed
    :param on_press: A callback function of one argument called when the button is pressed  (optional).

    Attributes:

    .. attribute:: label

        The label of the button (a string).

    Accepted events:

    .. method:: on_mouse_press

        Switches the state of the button.

    .. attribute:: [button, down], [button, up]:

        default path in the theme.

.. class:: OneTimeButton

    A :class:`Button` that changes back to its original state when the mouse is released.

    :param label: The string written in the button.
    :param on_release: A callback function of one argument called when the button is released (optional).

    Accepted events:

    .. method:: on_mouse_release

        Switches the state back and calls the callback if the mouse was released inside the button.

    .. attribute:: [button, down], [button, up]

        default path in the theme.

.. class:: Checkbox

     A button drawn as a checkbox icon with the label on the side.

    :param label: A string written in the button graphics.
    :param is_pressed: True if the button starts pressed
    :param on_press: A callback function of one argument called when the button is pressed  (optional).
    :param align: Whether the label is left or right of the checkbox.
    :param padding: The distance from the label to the checkbox.

    .. attribute:: ['checkbox', 'checked'], ['checkbox', 'unchecked']

        default path in the theme.
