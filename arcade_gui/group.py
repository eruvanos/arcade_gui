from typing import List

import PIL
import arcade
from arcade import Sprite, Texture
from arcade.gui import UIManager, UIElement, UIFlatButton

from arcade_gui.utils import DimensionMixin


class UIBox(UIElement):
    def __init__(self, width: int, height: int, color):
        super().__init__()

        image = PIL.Image.new('RGBA', (width, height), color)
        self.texture = Texture(f"Solid-{color[0]}-{color[1]}-{color[2]}", image, hit_box_algorithm='None')

    def render(self):
        pass


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

