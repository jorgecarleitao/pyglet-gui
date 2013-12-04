from setup import *

from pyglet_gui.dialog import Dialog
from pyglet_gui.option_selectors import Dropdown

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
