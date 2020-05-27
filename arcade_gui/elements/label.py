import arcade

from arcade_gui.elements import UIClickable
from arcade_gui.utils import get_text_image


class UILabel(UIClickable):
    def __init__(self,
                 parent: 'UIView',
                 text: str,
                 center_x: int,
                 center_y: int,
                 width: int = 0,

                 # own font object would be nice
                 font_size=22,
                 align="center",
                 font_name=('Calibri', 'Arial'),

                 font_color=arcade.color.GRAY,
                 font_color_hover=arcade.color.LIGHT_GRAY,
                 font_color_press=arcade.color.WHITE,

                 **kwargs):
        super().__init__(
            parent,
            center_x=center_x,
            center_y=center_y,
            **kwargs
        )
        self.style_classes.append('label')

        if font_color_hover is None:
            font_color_hover = font_color
        if font_color_press is None:
            font_color_press = font_color

        self.align = align
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.font_color_hover = font_color_hover
        self.font_color_press = font_color_press

        self.width = width
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render_texture()

    def render_texture(self):
        text_image_normal = get_text_image(text=self.text,
                                           font_color=self.font_color,
                                           font_size=self.font_size,
                                           font_name=self.font_name,
                                           align=self.align,
                                           width=int(self.width),
                                           )
        text_image_mouse_over = get_text_image(text=self.text,
                                               font_color=self.font_color_hover,
                                               font_size=self.font_size,
                                               font_name=self.font_name,
                                               align=self.align,
                                               width=int(self.width),
                                               )
        text_image_mouse_press = get_text_image(text=self.text,
                                                font_color=self.font_color_press,
                                                font_size=self.font_size,
                                                font_name=self.font_name,
                                                align=self.align,
                                                width=int(self.width),
                                                )

        self.normal_texture = arcade.Texture(image=text_image_normal, name=self.text + '1')
        self.press_texture = arcade.Texture(image=text_image_mouse_press, name=self.text + '2')
        self.hover_texture = arcade.Texture(image=text_image_mouse_over, name=self.text + '3')
