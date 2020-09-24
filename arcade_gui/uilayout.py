from _operator import attrgetter
from typing import NamedTuple, Dict, List, Union, Optional
from warnings import warn

import arcade
from arcade.gui import UILabel, UIElement, UIException

from arcade_gui.utils import DimensionMixin


class UILayoutManager(arcade.gui.UIManager):
    def __init__(self):
        super().__init__()

        self._root_layout: UILayout = AbsolutLayout()

    def add_ui_element(self, ui_element: UIElement):
        warn('Adding UIElements directly to a UILayoutManager can cause strange behaviour.')

    def _add_ui_element(self, ui_element: UIElement):
        return super().add_ui_element(ui_element)

    def set_root_layout(self, layout: 'UILayout'):
        """
        Set a new UILayout as the root Layout of the UIManager
        """
        self._root_layout = layout
        self.layout_refresh()

    def layout_refresh(self):
        self.purge_ui_elements()
        self._add_elements_from_layout(self._root_layout)

    def _add_elements_from_layout(self, layout: 'UILayout'):
        for element in layout:
            if isinstance(element, UIElement):
                self._add_ui_element(element)
            elif isinstance(element, UILayout):
                self._add_elements_from_layout(element)
            else:
                raise UIException('Layout only supports UIElement or UILayouts')


class PackedElement(NamedTuple):
    element: Union['UILayout', UIElement]
    data: Dict


class UILayout(DimensionMixin):
    def __init__(self, parent: Optional['UILayout'] = None):
        super().__init__()
        self.parent = parent
        self._elements: List[PackedElement] = []

    def pack(self, element: Union['UILayout', UIElement], **kwargs):
        self._elements.append(PackedElement(element, kwargs))

    def organize(self):
        for element, data in self._elements:
            self.organize_element(element, **data)

    def organize_element(self, element: UIElement, **kwargs):
        pass

    def __iter__(self):
        yield from map(attrgetter('element'), self._elements)


class AbsolutLayout(UILayout):
    pass


class UIBoxLayout(UILayout):
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

    def organize_element(self, element: Union['UILayout', UIElement], space=0, **kwargs):
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


class UIVerticalLayout(UIBoxLayout):
    def __init__(
            self,
    ) -> None:
        super().__init__(vertical=True)


class UIHorizontalLayout(UIBoxLayout):
    def __init__(
            self,
    ) -> None:
        super().__init__(vertical=False)
