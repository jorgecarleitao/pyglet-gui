Pyglet-gui at a glance
==========================

Pyglet gui was designed to make Graphical User Interfaces (GUI) in Pyglet. Here's an
overview of how you can write a GUI in Pyglet-gui.

First, a minimal Pyglet::

    import pyglet

    window = pyglet.window.Window(640, 480, resizable=True, vsync=True)
    batch = pyglet.graphics.Batch()

    @window.event
    def on_draw():
        window.clear()
        batch.draw()

Hello world
^^^^^^^^^^^^^

In Pyglet-gui, a GUI always need a :class:`~pyglet_gui.theme.theme.Theme`. Let's build one::

    from pyglet_gui.theme import Theme

    theme = Theme({"font": "Lucida Grande",
                   "font_size": 12,
                   "text_color": [255, 0, 0, 255]}, resources_path='')

Don't worry about the `resources_path=''` for now. With this theme, we can now create a simple
:class:`~pyglet_gui.gui.Label`::

    from pyglet_gui.gui import Label

    label = Label('Hello world')

Finally, we create a Manager to initialize a GUI and we run Pyglet app::

    from pyglet_gui.manager import Manager

    Manager(label, window=window, theme=theme, batch=batch)

    pyglet.app.run()

A Button
^^^^^^^^^^^^^^^

Let's say we now want a Button. Using the same Pyglet's setup, we create
a more complex Theme::

    from pyglet_gui.theme import Theme

    theme = Theme({"font": "Lucida Grande",
                   "font_size": 12,
                   "text_color": [255, 255, 255, 255],
                   "gui_color": [255, 0, 0, 255],
                   "button": {
                       "down": {
                           "image": {
                               "source": "button-down.png",
                               "frame": [8, 6, 2, 2],
                               "padding": [18, 18, 8, 6]
                           },
                           "text_color": [0, 0, 0, 255]
                       },
                       "up": {
                           "image": {
                               "source": "button.png",
                               "frame": [6, 5, 6, 3],
                               "padding": [18, 18, 8, 6]
                           }
                       }
                   }
                  }, resources_path='theme/')

This is assigning textures for the up and down state of the button.

Compared to the previous example, we added "gui_color" (color of non-text elements) and "button" to the root, and
resources_path='theme/'. This assumes the image "button.png" and "button-down.png" are
in the directory "theme/" (use Pyglet-gui ones for now).

Again::

    from pyglet_gui.buttons import Button

    # just to print something to the console, is optional.
    def callback(is_pressed):
        print('Button was pressed to state', is_pressed)

    button = Button('Hello world', on_press=callback)

and we run::

    from pyglet_gui.manager import Manager

    Manager(button, window=window, theme=theme, batch=batch)

    pyglet.app.run()

This is the basic idea of Pyglet-gui: you set up a Theme and create the GUI.

The default path of the Pyglet-gui Button is "button"->"up" and "button"->"down", which,
in Pyglet-gui is, represented by lists: ["button", "up"] and ["button", "down"].

Modifying the button
^^^^^^^^^^^^^^^^^^^^^

Lets now assume we don't want the paths ["button", "up"] and ["button", "down"], but we want the path
["my_path", "up"] and ["my_path", "down"].
We do::

    from pyglet_gui.buttons import Button

    class MyButton(Button):
        def get_path(self):
            path = ['my_path']
            if self.is_pressed:
                path.append('down')
            else:
                path.append('up')
            return path

    button = MyButton('Hello world', on_press=callback)

Pyglet-gui is designed to be reusable. All elements in Pyglet-gui are designed to
be subclassed to fulfill the developer's need.

This is just part of the whole
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This was a minimal overview of how you use Pyglet-gui, but Pyglet-gui is more.
It provides a consistent API to define custom Themes, custom graphics,
and, most importantly, user interfaces.

The next logical step is to have an overview of what Pyglet-gui allows you to do.
Thanks for your interest!
