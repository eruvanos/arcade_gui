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

        y_slot = self.window.height // 4

        # left
        arcade_gui.UILabel(
            self,
            'UILabel',
            center_x=self.window.width // 4,
            center_y=y_slot * 3,
        )

        ui_input_box = arcade_gui.UIInputBox(
            self,
            center_x=self.window.width // 4,
            center_y=y_slot * 2,
            width=300
        )
        ui_input_box.text = 'UIInputBox'
        ui_input_box.cursor_index = len(ui_input_box.text)

        button_normal = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button11.png'))
        hovered_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button01.png'))
        pressed_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
        arcade_gui.UIImageButton(
            self,
            center_x=self.window.width // 4,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='UIImageButton'
        )

        # right
        arcade_gui.UIFlatButton(
            self,
            'FlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 1,
            width=250,
            height=20
        )
        arcade_gui.UIGhostFlatButton(
            self,
            'GhostFlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 2,
            width=250,
            height=20
        )


if __name__ == '__main__':
    arcade.Window(title='ARCADE_GUI').show_view(MyView())
    arcade.run()
