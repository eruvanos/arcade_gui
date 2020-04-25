from typing import Union, Tuple

import arcade

from arcade_gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE


class UIButton(UIElement):
    """ Text-based button """

    CLICKED = 'CLICKED'

    def __init__(self,
                 text,
                 center_x, center_y,
                 width, height,
                 font_size=18, font_face: Union[str, Tuple[str, ...]] = "Arial", font_color=arcade.color.BLACK,
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 hover_color=arcade.color.DARK_GRAY,
                 button_height=2,
                 theme=None, **kwargs):
        super().__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.button_height = button_height
        self.theme = theme
        self.font_color = font_color
        self.pressed = False
        self.hover = False

        if self.theme:
            self.normal_texture = self.theme.button_textures['normal']
            self.hover_texture = self.theme.button_textures['hover']
            self.clicked_texture = self.theme.button_textures['clicked']
            self.locked_texture = self.theme.button_textures['locked']
            self.font_size = self.theme.font_size
            self.font_name = self.theme.font_name
            self.font_color = self.theme.font_color
        else:
            self.font_size = font_size
            self.font_face = font_face
            self.face_color = face_color
            self.highlight_color = highlight_color
            self.hover_color = hover_color
            self.shadow_color = shadow_color
            self.font_name = font_face
        if self.font_color is None:
            self.font_color = self.face_color

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
        self.hover = True

    def on_unhover(self):
        self.hover = False

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

    def draw_color_theme(self):

        if self.hover:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.hover_color)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)

        if self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

    def draw_texture_theme(self):
        if self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)

    def on_draw(self):
        """ Draw the button """
        if self.theme:
            self.draw_texture_theme()
        else:
            self.draw_color_theme()

        arcade.draw_text(self.text, self.center_x, self.center_y,
                         self.font_color, font_size=self.font_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
