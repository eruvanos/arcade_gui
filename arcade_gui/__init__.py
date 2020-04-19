__version__ = '0.1.0'

MOUSE_PRESS = 'MOUSE_PRESS'
MOUSE_RELEASE = 'MOUSE_RELEASE'
MOUSE_SCROLL = 'MOUSE_SCROLL'
KEY_PRESS = 'KEY_PRESS'
KEY_RELEASE = 'KEY_RELEASE'

from arcade_gui.core import UIEvent, UIView
from arcade_gui.label import UILabel

__all__ = [
    UIEvent,
    UIView,
    UILabel
]
