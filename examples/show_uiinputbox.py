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

        box = arcade_gui.UIInputBox(text='hello',
                                    center_x=400,
                                    center_y=300,
                                    width=200,
                                    height=40)
        self.add_ui_element(box)

    def on_text(self, text):
        super().on_text(text)


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
