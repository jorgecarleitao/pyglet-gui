Pyglet-gui is an extension of [Pyglet](http://www.pyglet.org/) for graphical user interfaces (GUIs).
Thanks for checking it out.

This project started as a fork of [Kytten](https://code.google.com/p/kytten/),
but ended up being a new project by its own right since the API changed dramatically.

Main features
--------------

* Implements a controller-viewer pattern.

    Pyglet-gui uses the concept of "controllers" to handle window events and "viewers" to draw.

    For example, a Button is a subclass of a two-state controller and a viewer.

* Use of Mixins

    Pyglet-gui uses mixins for extending functionality of viewers and controllers.
    This increases code reusability and modularity.

    For example, mouse hovering behaviour is added with a HoveringMixin class.

* Implements an abstraction for graphical appearance

    Pyglet-gui uses "themes" where each (static) resource is defined in a JSON file.
    This file is loaded, and viewers select specific resources
    from an unique path.

    For example, the Pyglet-gui standard Button chooses the path

        def get_path(self):
            path = ['button']
            if self.is_pressed():
                path.append('down')
            else:
                path.append('up')
            return path

* Has some standard user interfaces:

    * Button, Slider
    * Option selector, Dropdown
    * Vertical, Horizontal, Grid containers.
    * Scrollable content display

Supported Versions
-------------------

* Python:

    * 2.7
    * 3.2
    * 3.3
    * 3.4

* Pyglet:

    * >= 1.2

Installation
--------------

1. Install Pyglet:

     pip install --upgrade http://pyglet.googlecode.com/archive/tip.zip

2. Install Pyglet-gui:

     pip install git+https://github.com/jorgecarleitao/pyglet-gui.git

Documentation
--------------

The documentation can be found in the [read the docs](http://pyglet-gui.readthedocs.org/en/latest/index.html).

Running tests
--------------

To run Pyglet-gui full test suite, use

    python -m tests.runtests

To run a specific module, use

    python -m tests.specificModule

Contributors
--------------

The contributor of Kytten was Conrad "Lynx" Wong, which this project reuses.

Jorge C. Leitão designed, unit tested and documented the API.
