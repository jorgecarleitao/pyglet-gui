# encoding: utf-8
from distutils.core import setup

setup(name='Pyglet-gui',
      version='0.1',
      description='An extension of pyglet for GUIs',
      long_description=open('README.md').read(),
      author='Jorge C. Leitão',
      url='https://github.com/jorgecarleitao/pyglet-gui',
      packages=('pyglet_gui', 'pyglet_gui.theme'),
      requires=('pyglet (>=1.2)',),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: MacOS X',
          'Environment :: Win32 (MS Windows)',
          'Environment :: X11 Applications',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Games/Entertainment',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
