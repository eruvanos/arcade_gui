import arcade
from arcade import View, Window
from arcade.gui import UILabel
from arcade.gui.ui_style import UIStyle

from arcade_gui.uilayout import UILayoutManager, UIBoxLayout


class UIView(View):
    def __init__(self):
        super().__init__()
        self.manager = UILayoutManager()

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

        root_layout = UIBoxLayout()
        root_layout.pack(UILabel(text="1. Red Sun", **defaults), space=15)
        root_layout.pack(UILabel(text="2. Green Gras", **defaults))
        root_layout.pack(UILabel(text="3. Blue Sky", **defaults), space=20)
        self.manager.set_root_layout(root_layout)

        layout = UIBoxLayout(vertical=False)
        layout.pack(UILabel(text="4. Red Sun", **defaults), space=15)
        layout.pack(UILabel(text="5. Green Gras", **defaults))
        layout.pack(UILabel(text="6. Blue Sky", **defaults), space=20)

        root_layout.pack(layout)

        self.layout = root_layout

    def on_draw(self):
        arcade.start_render()

        layout = self.layout
        l, r, t, b = layout.left, layout.right, layout.top, layout.bottom
        arcade.draw_lrtb_rectangle_outline(l, r, t, b, arcade.color.RED)


def main():
    window = Window()
    view = UIView()
    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()
