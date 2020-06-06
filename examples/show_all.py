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

    def on_show(self):
        print('on_show')
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4

        # left
        self.ui_manager.add_ui_element(arcade_gui.UILabel(
            'UILabel',
            center_x=self.window.width // 4,
            center_y=y_slot * 3,
        ))

        ui_input_box = arcade_gui.UIInputBox(
            center_x=self.window.width // 4,
            center_y=y_slot * 2,
            width=300
        )
        ui_input_box.text = 'UIInputBox'
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

        button_normal = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button11.png'))
        hovered_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button01.png'))
        pressed_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
        self.ui_manager.add_ui_element(arcade_gui.UIImageButton(
            center_x=self.window.width // 4,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='UIImageButton'
        ))

        # right
        self.ui_manager.add_ui_element(arcade_gui.UIFlatButton(
            'FlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 1,
            width=250,
            # height=20
        ))
        self.ui_manager.add_ui_element(arcade_gui.UIGhostFlatButton(
            'GhostFlatButton',
            center_x=self.window.width // 4 * 3,
            center_y=y_slot * 2,
            width=250,
            # height=20
        ))


if __name__ == '__main__':
    window = arcade.Window(title='ARCADE_GUI')
    window.show_view(MyView(window))
    arcade.run()
