from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from arcade_gui.utils import MColor

if TYPE_CHECKING:
    from arcade_gui import UIElement


def parse_color(color: str):
    """
    Parses the input string returning rgb int-tuple.

    Supported formats:

    * RGB ('r,g,b', 'r, g, b')
    * HEX ('00ff00')
    * Arcade colors ('BLUE', 'DARK_BLUE')

    """
    import arcade

    if hasattr(arcade.color, color.upper()):
        return getattr(arcade.color, color)
    elif len(color) == 6 and ',' not in color:
        return MColor.from_hex(color).rgb()
    elif len(color.split(',')) == 3:
        r, g, b = color.split(',')
        r = int(r.strip())
        g = int(g.strip())
        b = int(b.strip())
        return r, g, b
    else:
        return None


class UIStyle:
    """
    Used as singleton in the UIView, style changes are applied by changing the values of the singleton.

    Use `.load()` to update UIStyle instance from YAML-file


    """

    def __init__(self, data, *args, **kwargs):
        self.style = data

    def load(self, path: Path):
        """
        Load style from a file, overwriting existing data

        :param path:
        """
        with path.open() as file:
            self.style = yaml.safe_load(file)

    def _get(self, ui_element: 'UIElement', attr):
        element_style = getattr(ui_element, '_style', {})
        if attr in element_style:
            return element_style[attr]

        style_classes = reversed(ui_element.style_classes + [ui_element.id])
        for style_class in style_classes:
            style_data = self.style.get(style_class, {})
            attr_value = style_data.get(attr)
            if attr_value:
                return attr_value
        else:
            return None

    def get_color(self, ui_element, param):
        value = self._get(ui_element, param)
        if value:
            return parse_color(value)
        else:
            return None
