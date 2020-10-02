from typing import Union

import arcade
from arcade import View, Window
from arcade.gui import UILabel, UIElement
from arcade.gui.ui_style import UIStyle

from arcade_gui.uilayout import UILayoutManager, UILayout
from arcade_gui.uilayout.box import UIBoxLayout


class UIView(View):
    def __init__(self):
        super().__init__()
        self.manager = UILayoutManager()

        self._last_mouse_pos = (0, 0)

    def on_show_view(self):
        defaults = dict(
            center_x=0,
            center_y=0,
        )

        arcade.set_background_color(arcade.color.WHITE)

        style = UIStyle.default_style()
        style.set_class_attrs(
            UILabel.__name__,
        )

        root_layout = self.manager.root_layout
        # root_layout.bg = UIBox(100, 100, arcade.color.LIGHT_BLUE)

        # top right
        layout_v_2 = UIBoxLayout()
        layout_v_2.pack(UILabel(text="1. Red Sun", **defaults))
        layout_v_2.pack(UILabel(text="2. Green Gras", **defaults))
        layout_v_2.pack(UILabel(text="3. Blue Sky", **defaults), space=20)
        root_layout.pack(layout_v_2, right=0, top=20)

        # window center
        # TODO

        # bottom center
        # TODO

        # bottom left
        layout2 = UIBoxLayout(vertical=False)
        layout2.pack(UILabel(text="4. Red Sun", **defaults))
        layout2.pack(UILabel(text="5. Green Gras", **defaults))
        layout2.pack(UILabel(text="6. Blue Sky", **defaults), space=20)
        root_layout.pack(layout2, left=0, bottom=10)

        self.manager.refresh()
        self.debug_layout(root_layout)

    def debug_layout(self, element: Union[UIElement, UILayout], prefix=''):
        print(
            f'{prefix}{type(element).__name__}: xywh: {element.left}, {element.top}, {element.width}, {element.height}')

        if isinstance(element, UILayout):
            for e in element:
                self.debug_layout(e, '\t' + prefix)

    def draw_borders(self, element: Union[UIElement, UILayout]):
        l, r, t, b = element.left, element.right, element.top, element.bottom
        arcade.draw_lrtb_rectangle_outline(l, r, t, b, arcade.color.RED)

        if isinstance(element, UILayout):
            for e in element:
                self.draw_borders(e)

    def on_draw(self):
        arcade.start_render()

        # self.draw_borders(self.manager.root_layout)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.S:
            print(self.window.get_location())
        elif symbol == arcade.key.M:
            print(self._last_mouse_pos)
        elif symbol == arcade.key.W:
            print('Window size', self.window.get_size())
        elif symbol == arcade.key.D:
            self.debug_layout(self.manager.root_layout)
        elif symbol == arcade.key.R:
            (self.manager.refresh())

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self._last_mouse_pos = (x, y)


def main():
    window = Window(resizable=True)

    if len(arcade.get_screens()) > 1:
        window.set_location(2012, 256)

    view = UIView()
    window.show_view(view)

    arcade.run()


if __name__ == '__main__':
    main()
