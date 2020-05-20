import arcade

from arcade_gui.elements import UIAbstractButton
from arcade_gui.utils import get_text_image


class UILabel(UIAbstractButton):
    def __init__(self, text,
                 center_x, center_y,
                 width: int = None,

                 font_name=('Calibri', 'Arial'),
                 font_size=22,
                 font_color=arcade.color.GRAY,
                 font_color_hover=None,
                 font_color_press=None,

                 align="center",
                 **kwargs):
        super().__init__(**kwargs)

        self.style_classes.append('label')

        if font_color_hover is None:
            font_color_hover = font_color
        if font_color_press is None:
            font_color_press = font_color

        self.set_style_attrs(font_name=font_name)
        self.set_style_attrs(font_size=font_size)
        self.set_style_attrs(font_color=font_color)
        self.set_style_attrs(font_color_hover=font_color)
        self.set_style_attrs(font_color_press=font_color)

        self.center_x = center_x
        self.center_y = center_y
        self.width = width  # TODO needed?
        if width is None:
            width = 0

        text_image_normal = get_text_image(text=text,
                                           text_color=font_color,
                                           font_size=font_size,
                                           font_name=font_name,
                                           align=align,
                                           width=width,
                                           )
        text_image_mouse_over = get_text_image(text=text,
                                               text_color=font_color_hover,
                                               font_size=font_size,
                                               font_name=font_name,
                                               align=align,
                                               width=width,
                                               )
        text_image_mouse_press = get_text_image(text=text,
                                                text_color=font_color_press,
                                                font_size=font_size,
                                                font_name=font_name,
                                                align=align,
                                                width=width,
                                                )

        self.normal_texture = arcade.Texture(image=text_image_normal, name=text)
        self.mouse_press_texture = arcade.Texture(image=text_image_mouse_press, name=text + "3")
        self.mouse_over_texture = arcade.Texture(image=text_image_mouse_over, name=text + "6")
        self.set_proper_texture()
