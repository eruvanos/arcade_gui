from typing import Union

from arcade.gui import UIElement

from arcade_gui.uilayout import UILayout


class UIBoxLayout(UILayout):
    def __init__(self, vertical=True, **kwargs):
        super().__init__(**kwargs)
        self.vertical = vertical

        self._cursor = 0, 0

    def refresh(self):
        self._cursor = 0, 0
        super().refresh()

    def place(self, element: Union['UILayout', UIElement], space=0, **kwargs):
        cx, cy = self._cursor
        print(f'Box.pack {self._cursor}')

        if self.vertical:
            cy -= space
            self._cursor = cx, cy - element.height
        else:
            cx += space
            self._cursor = cx + element.width, cy

        element.left = self.offset_x + cx
        element.top = self.offset_y + cy

#
# class UIVerticalLayout(UIBoxLayout):
#     def __init__(
#             self,
#             **kwargs
#     ) -> None:
#         super().__init__(vertical=True, **kwargs)
#
#
# class UIHorizontalLayout(UIBoxLayout):
#     def __init__(
#             self,
#             **kwargs
#     ) -> None:
#         super().__init__(vertical=False, **kwargs)
