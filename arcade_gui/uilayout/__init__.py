from _operator import attrgetter
from abc import ABC, abstractmethod
from typing import List, Union, Optional, NamedTuple, Dict
from warnings import warn

import arcade
from arcade.gui import UILabel, UIElement, UIException

from arcade_gui.uilayout.utils import OffsetDimensionMixin


class UILayoutParent(ABC):

    @property
    def top(self):
        raise NotImplementedError

    @property
    def bottom(self):
        raise NotImplementedError

    @property
    def left(self):
        raise NotImplementedError

    @property
    def right(self):
        raise NotImplementedError

    @abstractmethod
    def changed(self):
        """Refresh the layouting of all children"""
        raise NotImplementedError()


class UILayoutManager(UILayoutParent, arcade.gui.UIManager):
    def __init__(self, window=None, lazy_refresh=False):
        super().__init__(window=window)
        self.lazy_refresh = lazy_refresh

        from arcade_gui.uilayout.anchor import UIAnchorLayout
        self._root_layout: UILayout = UIAnchorLayout(parent=self)

    def register_handlers(self):
        """
        Registers handler functions (`on_...`) to :py:attr:`arcade.gui.UIElement`
        """
        # self.window.push_handlers(self) # Not as explicit as following
        self.window.push_handlers(
            self.on_resize,
            self.on_draw,
            self.on_mouse_press,
            self.on_mouse_release,
            self.on_mouse_scroll,
            self.on_mouse_motion,
            self.on_key_press,
            self.on_key_release,
            self.on_text,
            self.on_text_motion,
            self.on_text_motion_select,
        )

    def add_ui_element(self, ui_element: UIElement):
        warn('Adding UIElements directly to a UILayoutManager can cause strange behaviour.')
        self.root_layout.pack(ui_element)

    def _add_ui_element(self, ui_element: UIElement):
        return super().add_ui_element(ui_element)

    @property
    def root_layout(self):
        return self._root_layout

    @root_layout.setter
    def root_layout(self, layout):
        self._root_layout = layout
        layout.parent = self
        self.refresh()

    def changed(self):
        if not self.lazy_refresh:
            self.refresh()

    def refresh(self):
        self.purge_ui_elements()
        self._root_layout.refresh()
        self._add_elements_from_layout(self._root_layout)

    def on_resize(self, width, height):
        print('on resize')
        # self.root_layout.top = height
        # self.root_layout.right = width
        # self.root_layout.left = 0
        self.refresh()


    @property
    def left(self):
        return self.window.get_viewport()[0]

    @property
    def right(self):
        return self.window.get_viewport()[1]

    @property
    def bottom(self):
        return self.window.get_viewport()[2]

    @property
    def top(self):
        return self.window.get_viewport()[3]

    def _add_elements_from_layout(self, layout: 'UILayout'):
        for element in layout.elements_with_bg():
            if isinstance(element, UIElement):
                self._add_ui_element(element)
            elif isinstance(element, UILayout):
                self._add_elements_from_layout(element)
            else:
                raise UIException('Layout only supports UIElement or UILayouts')


class UILayout(OffsetDimensionMixin, UILayoutParent, ABC):
    parent: Optional[UILayoutParent] = None
    _bg: UIElement = None

    def __init__(self, offset_x=0, offset_y=0, parent=None, **kwargs):
        super().__init__()
        self.parent = parent

        self._elements: List[PackedElement] = []

        self._offset_x = offset_x
        self._offset_y = offset_y

    @property
    def offset_x(self):
        return self._offset_x

    @offset_x.setter
    def offset_x(self, value):
        self._offset_x = value
        # self.changed()

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value
        # self.changed()

    def pack(self, element: Union['UILayout', UIElement], **kwargs):
        self._elements.append(PackedElement(element, kwargs))
        self.place(element, **kwargs)

        if isinstance(element, UILayout):
            element.parent = self
        self.changed()

    def changed(self):
        print(f'{self}.changed()')
        if self.parent:
            self.parent.changed()

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value: UIElement):
        self._bg = value
        self.refresh_background()

    def refresh_background(self):
        if self.bg and len(self) > 0:
            self.bg.width = self.width
            self.bg.height = self.height
            self.bg.center_x = self.center_x
            self.bg.center_y = self.center_y

    def refresh(self):
        for element, data in self._elements:
            if isinstance(element, UILayout):
                element.refresh()

            self.place(element, **data)

        self.refresh_background()

    @abstractmethod
    def place(self, element: Union['UILayout', UIElement], **kwargs):
        raise NotImplementedError()

    def elements_with_bg(self):
        if self.bg:
            yield self.bg
        yield from self

    def __iter__(self):
        yield from map(attrgetter('element'), self._elements)

    def __len__(self):
        return len(self._elements)


class PackedElement(NamedTuple):
    element: Union['UILayout', UIElement]
    data: Dict
