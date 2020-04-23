import arcade

import arcade_gui


class MyButton(arcade_gui.UIButton):
    def on_press(self):
        print('Pressed')

    def on_release(self):
        print('Released')

    def on_click(self):
        print('Clicked')


class MyView(arcade_gui.UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        # If the view is shown multiple times, we should always start from scratch
        self.purge_ui_elements()
        arcade.set_background_color(arcade.color.WHITE)

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
