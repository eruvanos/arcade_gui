from uuid import uuid4

import arcade

from arcade_gui import UIClickable, UIView
from arcade_gui.utils import render_text_image


class UIAbstractFlatButton(UIClickable):
    def __init__(self,
                 parent: UIView,
                 text: str,
                 center_x: int,
                 center_y: int,
                 width: int = None,

                 align="center",
                 **kwargs):
        super().__init__(
            parent,
            center_x=center_x,
            center_y=center_y,
            **kwargs
        )

        # TODO load defaults from style

        font_name = ('Calibri', 'Arial')
        font_size = 22

        border_width = 2
        border_color = None
        border_color_hover = arcade.color.WHITE
        border_color_press = arcade.color.WHITE

        font_color = arcade.color.WHITE
        font_color_hover = arcade.color.WHITE
        font_color_press = arcade.color.BLACK

        DARK_GRAY = (21, 19, 21)
        bg_color = DARK_GRAY
        bg_color_hover = DARK_GRAY
        bg_color_press = arcade.color.WHITE

        vmargin = 15

        text_image_normal = render_text_image(
            text,
            font_size=22,
            font_name=font_name,
            align=align,
            valign='middle',
            bg_image=None,
            width=width,
            height=font_size + vmargin,
            indent=0,

            font_color=font_color,
            border_width=border_width,
            border_color=border_color,
            bg_color=bg_color,
        )
        text_image_hover = render_text_image(
            text,
            font_size=22,
            font_name=font_name,
            align=align,
            valign='middle',
            bg_image=None,
            width=width,
            height=font_size + vmargin,
            indent=0,

            font_color=font_color_hover,
            border_width=border_width,
            border_color=border_color_hover,
            bg_color=bg_color_hover,
        )
        text_image_press = render_text_image(
            text,
            font_size=font_size,
            font_name=font_name,
            align=align,
            valign='middle',
            bg_image=None,
            width=width,
            height=font_size + vmargin,
            indent=0,

            font_color=font_color_press,
            border_width=border_width,
            border_color=border_color_press,
            bg_color=bg_color_press,
        )

        self.normal_texture = arcade.Texture(image=text_image_normal, name=str(uuid4()))
        self.hover_texture = arcade.Texture(image=text_image_hover, name=str(uuid4()))
        self.press_texture = arcade.Texture(image=text_image_press, name=str(uuid4()))


class UIFlatButton(UIAbstractFlatButton):
    def __init__(self, parent, text, center_x, center_y, width: int = None, align="center", **kwargs):
        super().__init__(parent, text, center_x, center_y, width, align, **kwargs)
        self.style_classes.append('flatbutton')


class UIGhostFlatButton(UIAbstractFlatButton):
    def __init__(self, parent, text, center_x, center_y, width: int = None, align="center", **kwargs):
        super().__init__(parent, text, center_x, center_y, width, align, **kwargs)
        self.style_classes.append('ghostflatbutton')
