import arcade

from arcade_gui import UIButton


class UI3DButton(UIButton):
    def __init__(self, text, center_x, center_y, width, height, *args, **kwargs):
        super().__init__(text, center_x, center_y, width, height, *args, **kwargs)
        self.style_classes.append('ui3dbutton')

        self.font_size = 18
        self.font_face = "Arial"

        self.shadow_color = arcade.color.GRAY
        self.button_height = 2

    def draw_button(self):
        normal_color = self.find_color('normal_color')
        hover_color = self.find_color('hover_color')
        pressed_color = self.find_color('pressed_color')

        if self.hovered:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, hover_color)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, normal_color)

        if self.pressed:
            color = pressed_color
        else:
            color = self.shadow_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2 + self.button_height / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2 + self.button_height / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2 - self.button_height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2 - self.button_height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = pressed_color
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

    def on_draw(self):
        self.draw_button()
        self.draw_text()

    def draw_text(self):

        center_x = self.center_x
        center_y = self.center_y

        if self.pressed:
            center_x -= 2
            center_y += 2

        font_color = self.find_color('font_color')
        arcade.draw_text(self.text, center_x, center_y,
                         font_color, font_size=self.font_size,
                         font_name=self.font_face,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
