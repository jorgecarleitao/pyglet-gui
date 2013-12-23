from distutils.core import setup

setup(name='pyglet-gui',
      version='0.1',
      description='An extension of pyglet for GUIs',
      author='Jorge C. Leitão',
      url='https://github.com/jorgecarleitao/pyglet-gui',
      packages=['pyglet_gui', 'pyglet_gui.theme'],
      requires=['pyglet (>=1.2)']
)
