from operator import attrgetter
from typing import Union

from arcade.gui import UIElement

from arcade_gui.uilayout import UILayout


class UIBoxLayout(UILayout):
    def __init__(
            self,
            vertical=True,
            align='left',
            **kwargs
    ):
        super().__init__(**kwargs)
        self.align = align
        self.vertical = vertical

        self._cursor = 0, 0

    # def size_hint(self) -> SizeHint:
    #     return SizeHint(
    #         width=self._width,
    #         height=self._height,
    #     )

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
        # Places elemens next to each other in one direction
        # Algorithm uses self.left/self.top as the start point to place elements
        # 'cursor' marks the next placeable position (relative)

        # get min size and calc alignment offsets
        min_width, min_height = self.min_size()

        start_x = 0
        start_y = 0

        if self.vertical:
            if self.align in ('top', 'start', 'left'):
                pass
            elif self.align in ('center',):
                start_y = (self.height - min_height) // 2
            elif self.align in ('bottom', 'end', 'right'):
                start_y = (self.height - min_height)
        else:  # horizontal
            start_y = (self.height - min_height)

            if self.align in ('top', 'start', 'left'):
                pass
            elif self.align in ('center',):
                start_x = (self.width - min_width) // 2
            elif self.align in ('bottom', 'end', 'right'):
                start_x = (self.width - min_width)

        # cursor: placeable position relative to self.left, self.top
        cursor = start_x, start_y

        # place elements
        for element, data in self._elements:
            cx, cy = cursor
            space = data.get('space', 0)

            # update cursor
            if self.vertical:
                cy += space
                cursor = cx, cy + element.height
            else:
                cx += space
                cursor = cx + element.width, cy

            # place element, invert bottom-top direction of arcade/OpenGL
            element.left = self.left + cx
            element.top = self.top - cy

    def min_size(self):
        width = 0
        height = 0
        for element, data in self._elements:
            width += element.width
            height += element.height

            if self.vertical:
                height += data.get('space', 0)
            else:
                width += data.get('space', 0)

        return width, height
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
