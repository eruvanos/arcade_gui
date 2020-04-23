import arcade

import arcade_gui


class MyView(arcade_gui.UIView):

    def __init__(self):
        super().__init__()

    def on_show(self):
        # If the view is shown multiple times, we should always start from scratch
        self.purge_ui_elements()
        arcade.set_background_color(arcade.color.WHITE)

        self.add_ui_element(arcade_gui.UILabel(
            'Hello world',
            x=self.window.width // 2,
            y=self.window.height // 2,
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
