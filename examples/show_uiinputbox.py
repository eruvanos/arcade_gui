import arcade

import arcade_gui
from arcade_gui import UIManager


class MyView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window
        self.ui_manager = UIManager(window)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)

    def on_show(self):
        print('on_show')
        self.setup()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        box = arcade_gui.UIInputBox(text='hello',
                                    center_x=400,
                                    center_y=300,
                                    width=200,
                                    height=40)
        self.ui_manager.add_ui_element(box)


if __name__ == '__main__':
    window = arcade.Window(title='ARCADE_GUI')
    window.show_view(MyView(window))
    arcade.run()
