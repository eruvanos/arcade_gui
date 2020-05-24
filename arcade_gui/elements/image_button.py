from uuid import uuid4

import arcade
from arcade import Texture

from arcade_gui import UIAbstractButton, utils


class UIImageButton(UIAbstractButton):
    def __init__(self,
                 center_x,
                 center_y,
                 normal_texture: Texture,
                 hover_texture: Texture,
                 press_texture: Texture,
                 text='',
                 **kwargs
                 ):
        super().__init__(
            center_x,
            center_y,
            **kwargs
        )

        self._normal_texture = normal_texture
        self._hover_texture = hover_texture
        self._press_texture = press_texture
        if text:
            self.render_with_text(text)
        else:
            self.normal_texture = normal_texture
            self.hover_texture = hover_texture
            self.press_texture = press_texture

        self.set_proper_texture()

    def render_with_text(self, text: str):
        font_color = arcade.color.GRAY
        font_size = 20

        normal_image = utils.get_image_with_text(text,
                                                 background_image=self._normal_texture.image,
                                                 text_color=font_color,
                                                 font_size=font_size,
                                                 align='center',
                                                 valign='middle'
                                                 )
        self.normal_texture = Texture(str(uuid4()), image=normal_image)

        hover_image = utils.get_image_with_text(text,
                                                background_image=self._hover_texture.image,
                                                text_color=font_color,
                                                font_size=font_size,
                                                align='center',
                                                valign='middle'
                                                )
        self.hover_texture = Texture(str(uuid4()), image=hover_image)

        press_image = utils.get_image_with_text(text,
                                                background_image=self._press_texture.image,
                                                text_color=font_color,
                                                font_size=font_size,
                                                align='center',
                                                valign='middle'
                                                )
        self.press_texture = Texture(str(uuid4()), image=press_image)
