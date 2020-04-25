import arcade

from arcade_gui import UIButton


class UI3DButton(UIButton):
    def draw_button(self):
        if self.hovered:
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

    def on_draw(self):
        self.draw_button()
        self.draw_text()

    def draw_text(self):

        center_x = self.center_x
        center_y = self.center_y

        if self.pressed:
            center_x -= 2
            center_y += 2

        arcade.draw_text(self.text, center_x, center_y,
                         self.font_color, font_size=self.font_size,
                         font_name=self.font_name,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")
