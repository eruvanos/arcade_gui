from dataclasses import dataclass

import arcade
import pytest

from arcade_gui.elements import UIBox
from arcade_gui.uilayout import UILayoutParent


def T(name, *args):
    return pytest.param(*args, id=name)


def dummy_element(width=100, height=50, color=arcade.color.LIGHT_CORAL):
    return UIBox(
        width=width,
        height=height,
        color=color
    )


@dataclass
class MockParent(UILayoutParent):
    top: int = 0
    bottom: int = 0
    left: int = 0
    right: int = 0

    def changed(self):
        pass
