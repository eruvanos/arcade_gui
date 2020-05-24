import arcade

import arcade_gui


class MyView(arcade_gui.UIView):

    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()

    def setup(self):
        self.purge_ui_elements()

        self.add_ui_element(arcade_gui.UILabel(
            'Hello world',
            center_x=self.window.width // 2,
            center_y=self.window.height // 2,
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.LIGHT_GRAY,
            font_color_press=arcade.color.GRAY,
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
