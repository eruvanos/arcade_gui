import colorsys

import arcade

from arcade_gui import UIButton, UIView


class MColor:
    def __init__(self, r: int, g: int, b: int):
        self.g = g
        self.r = r
        self.b = b

    @staticmethod
    def from_hex(color: str):
        r, g, b = MColor.hex_to_rgb(color)
        return MColor(r, g, b)

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        # noinspection PyTypeChecker
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return MColor(r, g, b)

    def adjust_darkness(self, factor):
        h, s, v = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        v = min(255, max(v * factor, 0))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return MColor(int(r), int(g), int(b))

    def __len__(self):
        return 3

    def __iter__(self):
        yield from self.rgb()

    def __getitem__(self, index):
        return self.rgb()[index]

    def rgb(self):
        return self.r, self.b, self.g


class GhostFlatButton(UIButton):
    def on_draw(self):
        """ Draw the button """

        font_color = arcade.color.BLACK

        primary_color = MColor.from_hex('#25A258').rgb()
        secondary_color = MColor.from_hex('#25A258').adjust_darkness(0.8).rgb()

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
                color=secondary_color,
            )

        elif self.hovered:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=primary_color,
            )

        arcade.draw_rectangle_outline(
            center_x=self.center_x,
            center_y=self.center_y + border_x_offset,
            width=self.width,
            height=button_height,
            color=primary_color,
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
    def on_draw(self):
        """ Draw the button """

        font_color = arcade.color.BLACK

        base_color = MColor.from_hex('#25A258')
        primary_color = base_color.rgb()
        secondary_color = base_color.adjust_darkness(1.1).rgb()
        tertiary_color = base_color.adjust_darkness(0.8).rgb()

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
                color=tertiary_color,
            )

        elif self.hovered:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=secondary_color,
            )
        else:
            arcade.draw_rectangle_filled(
                center_x=self.center_x,
                center_y=self.center_y + border_x_offset,
                width=self.width,
                height=button_height,
                color=primary_color,
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
