import arcade

import arcade_gui


class MyButton(arcade_gui.UI3DButton):
    def on_press(self):
        super().on_press()
        print('Pressed')

    def on_release(self):
        super().on_release()
        print('Released')

    def on_click(self):
        super().on_click()
        print('Clicked')


class MyView(arcade_gui.UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def setup(self):
        self.purge_ui_elements()

        self.add_ui_element(MyButton(
            'Hello world',
            center_x=self.window.width // 2,
            center_y=self.window.height // 2,
            width=200,
            height=40
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
