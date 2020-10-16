from typing import Union

from arcade.gui import UIElement

from arcade_gui.uilayout import UILayout, SizeHint


class UIAnchorLayout(UILayout):
    """

    Layout which places its children according to two anchor values
    (bottom|top and left|right).

    Supported pack options:
    - top|bottom: anchor on y axis
    - left|right: anchor on x axis
    - fill_x: fill x axis
    - fill_y: fill y axis

    """

    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)

        self._width = width
        self._height = height

    def size_hint(self) -> SizeHint:
        return SizeHint(
            width=self._width,
            height=self._height,
        )

    def place_elements(self):
        # TODO do not overdraw others!

        for element, data in self._elements:
            element: Union[UILayout, UIElement]
            top = data.get('top')
            left = data.get('left')
            bottom = data.get('bottom')
            right = data.get('right')
            center_x = data.get('center_x')
            center_y = data.get('center_y')

            fill_x = data.get('fill_x')
            fill_y = data.get('fill_y')

            if fill_x:
                element.width = self._width

            if fill_y:
                element.height = self._height

            if bottom is not None:
                element.bottom = self.parent.bottom + bottom
            elif top is not None:
                element.top = self.parent.top - top
            elif center_y is not None:
                element.center_y = self.parent.center_y + center_y

            if left is not None:
                element.left = self.parent.left + left
            elif right is not None:
                element.right = self.parent.right - right
            elif center_x is not None:
                element.center_x = self.parent.center_x + center_x
