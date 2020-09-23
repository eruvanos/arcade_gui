from _operator import attrgetter
from typing import NamedTuple, Dict, List

import arcade
from arcade import Window, View
from arcade.gui import UILabel, UIElement
from arcade.gui.ui_style import UIStyle


class UIManager(arcade.gui.UIManager):
    def add_layout(self, layout: 'Layout'):
        for element in layout:
            self.add_ui_element(element)


class UIView(View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()


class PackedElement(NamedTuple):
    element: UIElement
    data: Dict


class Layout:
    def __init__(self) -> None:
        super().__init__()
        self._elements: List[PackedElement] = []

    def pack(self, element, **kwargs):
        self._elements.append(PackedElement(element, kwargs))
        self.update(element, **kwargs)

    def update(self, element: UIElement, **kwargs):
        pass

    def __iter__(self):
        yield from map(attrgetter('element'), self._elements)


class ListLayout(Layout):
    def __init__(
            self,
            vertical=True
    ) -> None:
        super().__init__()
        self._vertical = vertical

        win = arcade.get_window()
        if vertical:
            self.cursor = win.width // 2, win.height
        else:
            self.cursor = 0, win.height // 2

    def update(self, element: UIElement, space=0, **kwargs):
        cx, cy = self.cursor

        if self._vertical:
            # add offset
            cy -= space
            # position element
            element.center_x = cx
            element.center_y = cy - space - element.height // 2
            # update cursor
            self.cursor = cx, cy - space - element.height
        else:
            # add offset
            cx += space
            # position element
            element.center_x = cx + space + element.width // 2
            element.center_y = cy
            # update cursor
            self.cursor = cx + space + element.width, cy


class VerticalLayout(ListLayout):
    def __init__(
            self,
    ) -> None:
        super().__init__(vertical=True)


class HorizontalLayout(ListLayout):
    def __init__(
            self,
    ) -> None:
        super().__init__(vertical=False)


def main():
    defaults = dict(
        center_x=0,
        center_y=0,
    )
    window = Window()
    view = UIView()

    style = UIStyle.default_style()
    style.set_class_attrs(
        UILabel.__name__,
    )

    layout = ListLayout()
    layout.pack(UILabel(text="1. Red Sun", **defaults), space=15)
    layout.pack(UILabel(text="2. Green Gras", **defaults))
    layout.pack(UILabel(text="3. Blue Sky", **defaults), space=20)
    view.manager.add_layout(layout)

    layout = ListLayout(vertical=False)
    layout.pack(UILabel(text="4. Red Sun", **defaults), space=15)
    layout.pack(UILabel(text="5. Green Gras", **defaults))
    layout.pack(UILabel(text="6. Blue Sky", **defaults), space=20)
    view.manager.add_layout(layout)

    window.show_view(view)
    arcade.run()


if __name__ == '__main__':
    main()
