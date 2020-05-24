import arcade
from PIL import ImageDraw

from arcade_gui import UIAbstractButton, UIView
from arcade_gui.utils import get_text_image, add_margin


class UIAbstractFlatButton(UIAbstractButton):
    def __init__(self,
                 text,
                 center_x, center_y,
                 width: int = None,

                 align="center",
                 **kwargs):
        super().__init__(**kwargs)

        # TODO load defaults from style

        font_name = ('Calibri', 'Arial')
        font_size = 22

        margin = (10, 15, 10, 15)

        border_width = 2
        border_color = None
        border_color_mouse_over = arcade.color.WHITE
        border_color_mouse_press = arcade.color.WHITE

        font_color = arcade.color.WHITE
        font_color_hover = arcade.color.WHITE
        font_color_press = arcade.color.BLACK

        DARK_GRAY = (21, 19, 21)
        bg_color = DARK_GRAY
        bg_color_hover = DARK_GRAY
        bg_color_press = arcade.color.WHITE

        # TODO set style attrs?
        # self.set_style_attrs(font_name=font_name)
        # self.set_style_attrs(font_size=font_size)
        # self.set_style_attrs(font_color=font_color)
        # self.set_style_attrs(font_color_hover=font_color_hover)
        # self.set_style_attrs(font_color_press=font_color_press)

        # TODO find_color crash, because parent view not available :/
        # font_color = self.find_color('font_color')
        # normal_color = self.find_color('normal_color')
        # hover_color = self.find_color('hover_color')
        # pressed_color = self.find_color('pressed_color')

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
                                           background_color=bg_color
                                           )
        text_image_mouse_over = get_text_image(text=text,
                                               text_color=font_color_hover,
                                               font_size=font_size,
                                               font_name=font_name,
                                               align=align,
                                               width=width,
                                               background_color=bg_color_hover
                                               )
        text_image_mouse_press = get_text_image(text=text,
                                                text_color=font_color_press,
                                                font_size=font_size,
                                                font_name=font_name,
                                                align=align,
                                                width=width,
                                                background_color=bg_color_press
                                                )

        # add margin
        text_image_normal = add_margin(text_image_normal,
                                       *margin,
                                       bg_color)
        text_image_mouse_over = add_margin(text_image_mouse_over,
                                           *margin,
                                           bg_color_hover)
        text_image_mouse_press = add_margin(text_image_mouse_press,
                                            *margin,
                                            bg_color_press)

        # draw outline
        rect = [0,
                0,
                text_image_normal.width - border_width / 2,
                text_image_normal.height - border_width / 2]

        if border_color and border_width:
            d = ImageDraw.Draw(text_image_normal)
            d.rectangle(rect, fill=None, outline=border_color, width=border_width)

        if border_color_mouse_over:
            d = ImageDraw.Draw(text_image_mouse_over)
            d.rectangle(rect, fill=None, outline=border_color_mouse_over, width=border_width)

        if border_color_mouse_press:
            d = ImageDraw.Draw(text_image_mouse_press)
            d.rectangle(rect, fill=None, outline=border_color_mouse_press, width=border_width)

        self.normal_texture = arcade.Texture(image=text_image_normal, name=text + "5")
        self.press_texture = arcade.Texture(image=text_image_mouse_press, name=text + "6")
        self.hover_texture = arcade.Texture(image=text_image_mouse_over, name=text + "7")
        self.set_proper_texture()


class UIFlatButton(UIAbstractFlatButton):
    def __init__(self, text, center_x, center_y, width: int = None, align="center", **kwargs):
        super().__init__(text, center_x, center_y, width, align, **kwargs)
        self.style_classes.append('flatbutton')


class UIGhostFlatButton(UIAbstractFlatButton):
    def __init__(self, text, center_x, center_y, width: int = None, align="center", **kwargs):
        super().__init__(text, center_x, center_y, width, align, **kwargs)
        self.style_classes.append('ghostflatbutton')


if __name__ == '__main__':
    view = UIView()
    window = arcade.Window(height=200, width=600)
    window.show_view(view)

    view.add_ui_element(UIFlatButton(
        'Hallo',
        center_x=100,
        center_y=100,
        width=150,
        height=20
    ))
    # view.add_ui_element(UIGhostFlatButton(
    #     'Hallo',
    #     center_x=300,
    #     center_y=100,
    #     width=150,
    #     height=20
    # ))

    arcade.set_background_color(arcade.color.WHITE)
    window.set_location(1200, 50)
    arcade.run()
