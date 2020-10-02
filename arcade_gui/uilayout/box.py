from operator import attrgetter
from typing import Union

from arcade.gui import UIElement

from arcade_gui.uilayout import UILayout


class UIBoxLayout(UILayout):
    def __init__(self, vertical=True, **kwargs):
        super().__init__(**kwargs)
        self.vertical = vertical

        self._cursor = 0, 0

    def pack(self, element: Union['UILayout', UIElement], **kwargs):
        super().pack(element, **kwargs)

        # TODO this change could be reflected in sizehint not in actual changed properties
        space = kwargs.get('space', 0)
        if self.vertical:
            self.width = max(map(attrgetter('width'), self))
            self.height += element.height + space
        else:
            self.height = max(map(attrgetter('height'), self))
            self.width += element.width + space

    def place_elements(self):
        cursor = 0, 0
        for element, data in self._elements:
            cx, cy = cursor
            space = data.get('space', 0)

            if self.vertical:
                cy -= space
                cursor = cx, cy - element.height
            else:
                cx += space
                cursor = cx + element.width, cy

            element.left = self.left + cx
            element.top = self.top + cy

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
