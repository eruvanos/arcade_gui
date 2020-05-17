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
            'UILabel',
            center_x=self.window.width // 4,
            center_y=y_slot * 3,
        ))
        ui_input_box = arcade_gui.UIInputBox(
            center_x=self.window.width // 4,
            center_y=y_slot * 2,
        )
        ui_input_box.text = 'UIInputBox'
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.add_ui_element(ui_input_box)

        button_normal = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button11.png'))
        hovered_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button01.png'))
        pressed_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
        self.add_ui_element(arcade_gui.UIImageButton(
            center_x=self.window.width // 4,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hovered_texture=hovered_texture,
            pressed_texture=pressed_texture,
            text='UIImageButton'
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
