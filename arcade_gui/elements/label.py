import arcade

from arcade_gui.elements import UIAbstractButton
from arcade_gui.utils import get_text_image


class UILabel(UIAbstractButton):
    def __init__(self, text,
                 center_x, center_y,
                 width: int = 0,

                 font_name=('Calibri', 'Arial'),
                 font_size=22,
                 font_color=arcade.color.GRAY,
                 font_color_hover=None,
                 font_color_press=None,

                 align="center",
                 **kwargs):
        super().__init__(center_x=center_x, center_y=center_y, width=width, **kwargs)

        self.style_classes.append('label')

        if font_color_hover is None:
            font_color_hover = font_color
        if font_color_press is None:
            font_color_press = font_color

        self.font_size = font_size
        self.font_name = font_name

        self.font_color = font_color
        self.font_color_hover = font_color_hover
        self.font_color_press = font_color_press

        self.align = align
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
                                           text_color=self.font_color,
                                           font_size=self.font_size,
                                           font_name=self.font_name,
                                           align=self.align,
                                           width=int(self.width),
                                           )
        text_image_mouse_over = get_text_image(text=self.text,
                                               text_color=self.font_color_hover,
                                               font_size=self.font_size,
                                               font_name=self.font_name,
                                               align=self.align,
                                               width=int(self.width),
                                               )
        text_image_mouse_press = get_text_image(text=self.text,
                                                text_color=self.font_color_press,
                                                font_size=self.font_size,
                                                font_name=self.font_name,
                                                align=self.align,
                                                width=int(self.width),
                                                )

        self.normal_texture = arcade.Texture(image=text_image_normal, name=self.text + '1')
        self.press_texture = arcade.Texture(image=text_image_mouse_press, name=self.text + '2')
        self.hover_texture = arcade.Texture(image=text_image_mouse_over, name=self.text + '3')
        self.set_proper_texture()
