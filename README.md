Pyglet-gui is an extension of [Pyglet](http://www.pyglet.org/) for graphical user interfaces (GUIs).
Thanks for checking it out.

This project started as a fork of [Kytten](https://code.google.com/p/kytten/),
but ended up being a new project by its own right since the API changed dramatically.

This project is in pre-alpha.

Main features
--------------

* Implements a controller-viewer pattern.

    Pyglet-gui uses the concept of "controllers" to handle window events and "viewers" to draw.

    We provide both low-level interfaces such as two-state controllers,
    and end-user interfaces such as buttons, both of which designed to be extended
    to the user's need.

    For example, a Button is a subclass of a two-state controller and a viewer.

* Use of Mixins

    Pyglet-gui uses mixins for extending functionality of viewers and controllers.
    This increases code reusability and modularity.

    For example, you add mouse hovering behaviour to a button by mixin a Button with a HoveringMixin.

* Implements an abstraction for graphical appearance

    Pyglet-gui uses the concept of "theme", on which each (static) resource is defined in a JSON file.
    This file is loaded into a list of factories, a Theme, and viewers can load specific resources
    by choosing the factory they want by a path.

    For example, a Button chooses the path

        def get_path(self):
            path = ['button']
            if self.is_pressed():
                path.append('down')
            else:
                path.append('up')
            return path

    and the factory produces a vertex list and a texture from the specifications in the JSON file.

Installation
--------------

1. Get a copy of the source from [GitHub](https://github.com/jorgecarleitao/pyglet-gui).

2. python setup.py install


Documentation
--------------

The documentation is incomplete, but being

The documentation can be found in the [read the docs](http://pyglet-gui.readthedocs.org/en/latest/index.html).

Running tests
--------------

You can run the test suite of pyglet-gui from the root using

    python -m tests.runtests

If you just want to run a specific module, you can use

    python -m tests.specificModule

Contributors
--------------

The contributor of Kytten was Conrad "Lynx" Wong, which this project reuses.

Jorge C. Leitão designed, tested and documented the API.
