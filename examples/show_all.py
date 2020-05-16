import arcade

import arcade_gui


class MyView(arcade_gui.UIView):

    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup()

    def setup(self):
        self.purge_ui_elements()

        y_slot = self.window.height // 4

        # left
        self.add_ui_element(arcade_gui.UILabel(
            'Hello world',
            center_x=self.window.width // 4,
            center_y=y_slot * 3,
        ))
        self.add_ui_element(arcade_gui.UIInputBox(
            center_x=self.window.width // 4,
            center_y=y_slot * 2,
        ))

        # right
        self.add_ui_element(arcade_gui.UIFlatButton(
            'FlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 1,
            width=200,
            height=20
        ))
        self.add_ui_element(arcade_gui.UIGhostFlatButton(
            'GhostFlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 2,
            width=200,
            height=20
        ))

        self.add_ui_element(arcade_gui.UI3DButton(
            'UI3DButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 3,
            width=200,
            height=40
        ))


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
