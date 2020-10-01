from typing import Union

from arcade.gui import UIElement

from arcade_gui.uilayout import UILayout


class UIAnchorLayout(UILayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def place(
            self,
            element: Union['UILayout', UIElement],
            top: int = None,
            left: int = None,
            bottom: int = None,
            right: int = None,
            **kwargs):
        print(f'Anchor.place {element}')
        if bottom is not None:
            element.bottom = self.parent.bottom + bottom
        elif top is not None:
            element.top = self.parent.top - top

        if left is not None:
            element.left = self.parent.left + left
        elif right is not None:
            element.right = self.parent.right - right
