from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.option_selectors import Dropdown
from pyglet_gui.theme import Theme

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "dropdown": {
                   "pulldown": {
                       "image": {
                           "source": "pulldown.png",
                           "frame": [3, 3, 10, 10],
                           "padding": [4, 4, 4, 4]
                       }
                   },
                   "image": {
                       "source": "dropdown.png",
                       "frame": [4, 8, 20, 5],
                       "padding": [6, 10, 6, 10]
                   }
               },
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
               },
               "vscrollbar": {
                   "knob": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 16, 16, 16],
                           "frame": [0, 6, 16, 4],
                           "padding": [0, 0, 0, 0]
                       },
                       "offset": [0, 0]
                   },
                   "bar": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 64, 16, 16]
                       },
                       "padding": [0, 0, 0, 0]
                   }
               }
              }, resources_path='../theme')

# Set up a Dialog
dialog = Dialog(
    Dropdown(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon',
              'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa',
              'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron',
              'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon',
              'Phi', 'Chi', 'Psi', 'Omega']),
    window=window,
    batch=batch,
    theme=theme)

pyglet.app.run()
