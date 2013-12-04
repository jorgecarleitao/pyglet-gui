Pyglet-gui is an extension of pyglet for graphical user interfaces.
Thanks for checking it out.

This project started as a fork of Kytten (https://code.google.com/p/kytten/),
but ended up being a new project since the API changed dramatically.

Main features
==============

* Implements the controller-viewer pattern.

Pyglet-gui uses the concept of "Controllers" to handle events and "Widgets" to draw.

It provides both low-level interfaces, such as two-state controllers,
and end-user interfaces, such as buttons, for controllers and viewers,
which can be further extended.

* Use of Mixins

Pyglet-gui uses mixins for extending functionality of viewers and controllers.
This minimizes repetition and increases code reusability.

* Implements an abstraction for graphical appearance

Pyglet-gui uses the concept of "theme", on which each (static) resource is defined in a JSON file.
This file is loaded into a "theme" which is used by widgets to load resources.

This decouples the laying out of elements from its graphical appearance. You can create your own themes,
or extend the existing one.


Installation
=============

1. Get a copy of the source from github.

2. Copy the source to the working directory of your project.


Documentation
=============

The documentation can be found in the [read the docs](https://readthedocs.org/builds/pyglet-gui/).

Contributors
=============

The main contributor was Conrad "Lynx" Wong for the code of Kytten.

Jorge C. Leitão re-formulated the API.
