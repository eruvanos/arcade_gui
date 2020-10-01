from typing import List

import arcade
from arcade.gui import UIManager, UIElement, UIFlatButton

from arcade_gui import UIBox
from arcade_gui.uilayout.utils import DimensionMixin


class UIGroup(DimensionMixin):
    def __init__(
            self,
            margin=(0, 0, 0, 0),
            bg_color=arcade.color.ASH_GREY
    ):
        self.elements: List[UIElement] = []

        if isinstance(margin, int):
            margin = (margin, margin, margin, margin)

        self.margin_top, self.margin_right, self.margin_bottom, self.margin_left = margin
        self.bg_color = bg_color

    def __iter__(self):
        return iter(self.elements)

    def add_element(self, element: UIElement):
        self.elements.append(element)

    def add_to_ui(self, ui_manager: UIManager):
        # Background
        background = UIBox(self.width, self.height, self.bg_color)
        background.position = self.position
        self.elements.insert(0, background)

        # Close Button
        exit_button = UIFlatButton(
            'X',
            int(self.right - 40 - self.margin_right), int(self.top - 40 - self.margin_top),
            width=40, height=40
        )
        exit_button.on_click = self.close
        self.elements.append(exit_button)

        for element in self.elements:
            ui_manager.add_ui_element(element)

    def close(self):
        for element in self.elements:
            element.remove_from_sprite_lists()
