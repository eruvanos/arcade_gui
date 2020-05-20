import arcade
from pyglet.image import Texture

from arcade_gui import UIAbstractButton


class UIImageButton(UIAbstractButton):

    def __init__(self,
                 center_x,
                 center_y,
                 normal_texture: Texture,
                 hovered_texture: Texture,
                 pressed_texture: Texture,
                 text='',
                 **kwargs
                 ):
        self.normal_texture = normal_texture
        self.hovered_texture = hovered_texture
        self.pressed_texture = pressed_texture

        width = min(
            self.normal_texture.width,
            self.hovered_texture.width,
            self.pressed_texture.width,
        )
        height = min(
            self.normal_texture.height,
            self.hovered_texture.height,
            self.pressed_texture.height,
        )

        super().__init__(
            text,
            center_x,
            center_y,
            width,
            height,
            **kwargs
        )

    def on_draw(self):
        if self.pressed:
            arcade.draw_texture_rectangle(
                self.center_x,
                self.center_y,
                self.width,
                self.height,
                self.pressed_texture
            )
        elif self.hovered:
            arcade.draw_texture_rectangle(
                self.center_x,
                self.center_y,
                self.width,
                self.height,
                self.hovered_texture
            )
        else:
            arcade.draw_texture_rectangle(
                self.center_x,
                self.center_y,
                self.width,
                self.height,
                self.normal_texture
            )

        if self.text:
            font_color = self.find_color('font_color')

            arcade.draw_text(self.text,
                             self.center_x, self.center_y,
                             font_color,
                             width=self.width,
                             font_size=20,
                             align='center',
                             anchor_x="center", anchor_y="center"
                             )
