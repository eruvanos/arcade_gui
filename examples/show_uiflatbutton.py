import arcade

import arcade_gui
from arcade_gui import UIFlatButton, UIGhostFlatButton


class MyView(arcade_gui.UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def setup(self):
        self.purge_ui_elements()
        self.add_ui_element(UIFlatButton(
            'Hello world',
            center_x=200,
            center_y=self.window.height // 2,
            width=200,
            height=40
        ))

        self.add_ui_element(UIGhostFlatButton(
            'Hello world',
            center_x=600,
            center_y=self.window.height // 2,
            width=200,
            height=40
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
