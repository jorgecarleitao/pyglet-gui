Pyglet-gui is an extension of [Pyglet](http://www.pyglet.org/) for graphical user interfaces (GUIs).
Thanks for checking it out.

This project started as a fork of [Kytten](https://code.google.com/p/kytten/),
but ended up being a new project by its own right since the API changed dramatically.

This project is in pre-alpha.

Main features
--------------

* Implements the controller-viewer pattern.

    Pyglet-gui uses the concept of "Controllers" to handle events and "Widgets" to draw.

    It provides both low-level interfaces, such as two-state controllers,
    and end-user interfaces, such as buttons,
    which can be further extended.

* Use of Mixins

    Pyglet-gui uses mixins for extending functionality of viewers and controllers.
    This minimizes repetition and increases code reusability.

* Implements an abstraction for graphical appearance

    Pyglet-gui uses the concept of "theme", on which each (static) resource is defined in a JSON file.
    This file is loaded into a "theme" that is used by widgets to load resources.

    This decouples the laying out of elements from its graphical appearance. You can create your own themes,
    or extend the existing one.


Installation
--------------

1. Get a copy of the source from [GitHub](https://github.com/jorgecarleitao/pyglet-gui).

2. Copy the source to the working directory of your project.


Documentation
--------------

(Under construction)

The documentation can be found in the [read the docs](https://readthedocs.org/builds/pyglet-gui/).

Contributors
--------------

The contributor of Kytten was Conrad "Lynx" Wong, which this project reuses.

Jorge C. Leitão re-formulated the API.
