import arcade

import arcade_gui


class MyView(arcade_gui.UIView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        # If the view is shown multiple times, we should always start from scratch
        self.purge_ui_elements()
        arcade.set_background_color(arcade.color.WHITE)

        self.add_ui_element(arcade_gui.UIInputBox(
            x=400,
            y=300,
            width=200,
            height=40
        ))

    def on_text(self, text):
        super().on_text(text)
        print()


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
