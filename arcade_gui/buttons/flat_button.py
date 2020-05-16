import arcade

from arcade_gui import UIButton, UIView


class GhostFlatButton(UIButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style_classes.append('ghostflatbutton')


    def on_draw(self):
        """ Draw the button """
        font_color = self.find_color('font_color')

        normal_color = self.find_color('normal_color')
        hover_color = self.find_color('hover_color')
        pressed_color = self.find_color('pressed_color')

        font_size = 20
        button_height = font_size * 2
        border_width = 3
        border_x_offset = +2

        if self.pressed:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=pressed_color,
            )

        elif self.hovered:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=hover_color,
            )

        arcade.draw_rectangle_outline(
            center_x=self.center_x,
            center_y=self.center_y + border_x_offset,
            width=self.width,
            height=button_height,
            color=normal_color,
            border_width=border_width,
        )

        arcade.draw_text(
            self.text,
            self.center_x,
            self.center_y,
            font_color,
            font_size=font_size,
            font_name=('calibri', 'arial'),
            width=self.width, align="center",
            anchor_x="center", anchor_y="center")


class FlatButton(UIButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style_classes.append('flatbutton')

    def on_draw(self):
        """ Draw the button """
        font_color = self.find_color('font_color')

        normal_color = self.find_color('normal_color')
        hover_color = self.find_color('hover_color')
        pressed_color = self.find_color('pressed_color')

        font_size = 20
        button_height = font_size * 2
        border_x_offset = +2

        if self.pressed:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=pressed_color,
            )

        elif self.hovered:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=hover_color,
            )
        else:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=normal_color,
            )

        arcade.draw_text(
            self.text,
            self.center_x,
            self.center_y,
            font_color,
            font_size=font_size,
            font_name=('calibri', 'arial'),
            width=self.width, align="center",
            anchor_x="center", anchor_y="center")


if __name__ == '__main__':
    view = UIView()
    window = arcade.Window(height=200, width=600)
    window.show_view(view)

    view.add_ui_element(FlatButton(
        'Hallo',
        center_x=100,
        center_y=100,
        width=150,
        height=20
    ))
    view.add_ui_element(GhostFlatButton(
        'Hallo',
        center_x=300,
        center_y=100,
        width=150,
        height=20
    ))

    arcade.set_background_color(arcade.color.WHITE)
    window.set_location(1200, 50)
    arcade.run()
