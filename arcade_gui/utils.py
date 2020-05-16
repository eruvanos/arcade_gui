import colorsys
import os
import sys
from pathlib import Path
from typing import Union


def create_resource_path(relative_path: Union[str, Path]):
    """
    Get absolute path to resource, works for dev and for PyInstaller's 'onefile' mode

    :param relative_path: A relative path to a file of some kind.

    """

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # pylint: disable=no-member,protected-access
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MColor:
    # TODO do we really need this?
    def __init__(self, r: int, g: int, b: int):
        self.g = g
        self.r = r
        self.b = b

    @staticmethod
    def from_hex(color: str):
        r, g, b = MColor.hex_to_rgb(color)
        return MColor(r, g, b)

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        # noinspection PyTypeChecker
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return MColor(r, g, b)

    def adjust_darkness(self, factor):
        h, s, v = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        v = min(255, max(v * factor, 0))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return MColor(int(r), int(g), int(b))

    def __len__(self):
        return 3

    def __iter__(self):
        yield from self.rgb()

    def __getitem__(self, index):
        return self.rgb()[index]

    def rgb(self):
        return self.r, self.b, self.g
