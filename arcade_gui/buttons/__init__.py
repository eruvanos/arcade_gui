from typing import Union, Tuple

import arcade

from arcade_gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE
from arcade_gui.ui_style import UIStyle


class UIButton(UIElement):
    """ Text-based button """

    CLICKED = 'CLICKED'

    def __init__(self,
                 text,
                 center_x, center_y,
                 width, height,
                 **kwargs):
        super().__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text

        self.pressed = False
        self.hovered = False

    def find_color(self, param):
        paren_theme = self.parent_style()
        return paren_theme.get_color(self, param)

    def on_event(self, event: UIEvent):
        if event.type == MOUSE_PRESS and self.hover_point(event.x, event.y):
            self.pressed = True
            self.on_press()
        elif event.type == MOUSE_RELEASE and self.pressed:
            if self.pressed:
                self.pressed = False
                self.on_release()

                if self.hover_point(event.x, event.y):
                    self.on_click()
                    self.view.on_event(UIEvent(UIButton.CLICKED, ui_element=self))

    def on_hover(self):
        self.hovered = True

    def on_unhover(self):
        self.hovered = False

    def on_press(self):
        pass

    def on_release(self):
        pass

    def on_click(self):
        pass

    def hover_point(self, hover_x: float, hover_y: float) -> bool:
        if hover_x > self.center_x + self.width / 2:
            return False
        if hover_x < self.center_x - self.width / 2:
            return False
        if hover_y > self.center_y + self.height / 2:
            return False
        if hover_y < self.center_y - self.height / 2:
            return False

        return True
