import arcade

import arcade_gui
from arcade_gui import UIFlatButton, UIGhostFlatButton
from arcade_gui.ui_style import UIStyle


class MyView(arcade_gui.UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()

    def setup(self):
        self.purge_ui_elements()
        flat = UIFlatButton('Hello world', center_x=200, center_y=self.window.height // 2, width=200, height=40)
        flat.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(51, 139, 57),
            bg_color_hover=(51, 139, 57),
            bg_color_press=(28, 71, 32),
            border_color=(51, 139, 57),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.add_ui_element(flat)

        # creates a new class, which will match the id
        UIStyle.default_style().set_class_attrs(
            'right_button',
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=(135, 21, 25),
            bg_color_hover=(135, 21, 25),
            bg_color_press=(122, 21, 24),
            border_color=(135, 21, 25),
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.add_ui_element(UIGhostFlatButton(
            'Hello world',
            center_x=600,
            center_y=self.window.height // 2,
            width=200,
            height=40,
            id='right_button'
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
