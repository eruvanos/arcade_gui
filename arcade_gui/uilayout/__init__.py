from _operator import attrgetter
from abc import ABC, abstractmethod
from typing import List, Union, Optional, NamedTuple, Dict
from warnings import warn

import arcade
from arcade import SpriteList
from arcade.gui import UILabel, UIElement

from arcade_gui.uilayout.utils import OffsetDimensionMixin


class SizeHint(NamedTuple):
    width: int
    height: int


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

    @property
    def center_x(self):
        return self.left + (self.right - self.left) // 2

    @property
    def center_y(self):
        return self.bottom + (self.top - self.bottom) // 2

    @abstractmethod
    def changed(self):
        """Refresh the layouting of all children"""
        raise NotImplementedError()


class UILayoutManager(UILayoutParent, arcade.gui.UIManager):
    def __init__(self, window=None):
        super().__init__(window=window)

        from arcade_gui.uilayout.anchor import UIAnchorLayout
        self._root_layout: UILayout = UIAnchorLayout(
            self.window.width,
            self.window.height,
            parent=self)

        self._changed = False
        self._ui_elements: SpriteList = SpriteList(use_spatial_hash=False)

    def on_draw(self):
        super().on_draw()
        self._root_layout.draw()

    def on_update(self, dt):
        if self._changed:
            # warn('Refresh UILayout in update')
            self.root_layout.width = self.window.width
            self.root_layout.height = self.window.height
            self.refresh()

    def add_ui_element(self, ui_element: UIElement):
        warn('Adding UIElements directly to a UILayoutManager can cause strange behaviour.')
        super().add_ui_element(ui_element)

    def _add_ui_element(self, ui_element: UIElement):
        return super().add_ui_element(ui_element)

    @property
    def root_layout(self):
        return self._root_layout

    @root_layout.setter
    def root_layout(self, layout: 'UILayout'):
        self._root_layout = layout
        layout.parent = self
        self.refresh()

    def changed(self):
        self._changed = True

    def refresh(self):
        self._changed = False
        self._root_layout.refresh()

        if not self._root_layout.valid():
            warn('Refresh produced invalid boundaries')

    def on_resize(self, width, height):
        self.changed()

    # UILayoutManager always fills the whole view
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


class PackedElement(NamedTuple):
    element: Union['UILayout', UIElement]
    data: Dict


class UILayout(UILayoutParent, ABC):
    _bg: UIElement = None

    def __init__(self,
                 parent: Optional[UILayoutParent] = None,
                 draw_border=False,
                 id=None,
                 **kwargs):
        super().__init__()
        # self.draw_border = draw_border
        self._parent: Optional[UILayoutParent] = parent

        self._elements: List[PackedElement] = []
        self._layer = SpriteList()
        self._child_layouts = []

        # own position
        self._top = 0
        self._left = 0

        self._width = 0
        self._height = 0
        self._id = id

    @property
    def id(self):
        return self._id

    def valid(self):
        left = self.left
        right = self.right
        top = self.top
        bottom = self.bottom

        if not (left <= right):
            return False
        if not (bottom <= top):
            return False

        for element, data in self._elements:
            if not (left <= element.left <= right):
                return False
            if not (left <= element.right <= right):
                return False
            if not (bottom <= element.top <= top):
                return False
            if not (bottom <= element.bottom <= top):
                return False

            if isinstance(element, UILayout):
                if not element.valid():
                    return False

        return True

    # ---------- propergate parent
    @property
    def parent(self) -> Optional[UILayoutParent]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional[UILayoutParent]):
        self._parent = value
        for child in self._child_layouts:
            child.parent = value

    # --------- add element & size hint
    def pack(self, element: Union['UILayout', UIElement], **kwargs):
        self._elements.append(PackedElement(element, kwargs))

        if isinstance(element, UIElement):
            self._layer.append(element)
        if isinstance(element, UILayout):
            element.parent = self
            self._child_layouts.append(element)

        # self.update_size_hint()
        self.changed()

    def draw(self):
        # TODO fix this!
        self.draw_border()

        self._layer.draw()
        self._layer.draw_hit_boxes(arcade.color.LIGHT_RED_OCHRE, 2)
        for child in self._child_layouts:
            child.draw()

    def draw_border(self):
        arcade.draw_lrtb_rectangle_outline(
            self.left,
            self.right,
            self.top,
            self.bottom,
            arcade.color.LIGHT_RED_OCHRE)

    # def update_size_hint(self):
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def size_hint(self) -> SizeHint:
    #     raise NotImplementedError()

    # @staticmethod
    # def size_hint_of(element: Union['UILayout', UIElement]):
    #     if isinstance(element, UILayout):
    #         return element.size_hint()
    #     else:
    #         return SizeHint(
    #             width=int(element.width),
    #             height=int(element.height),
    #             fill_x=False,
    #             fill_y=False
    #         )

    # --------- position - fixed
    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        y_diff = value - self.top
        self.move(0, y_diff)

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @left.setter
    def left(self, value):
        x_diff = value - self.left
        self.move(x_diff, 0)

    @property
    def width(self):
        """ minimal width """
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """ minimal height """
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    # --------- position - calc
    @property
    def right(self):
        return self.left + self.width

    @right.setter
    def right(self, value):
        x_diff = value - self.right
        self.move(x_diff, 0)

    @property
    def bottom(self):
        return self.top - self.height

    @bottom.setter
    def bottom(self, value):
        y_diff = value - self.bottom
        self.move(0, y_diff)

    @property
    def center_x(self):
        return self.left + (self.right - self.left) // 2

    @center_x.setter
    def center_x(self, value):
        x_diff = value - self.center_x
        self.move(x_diff, 0)

    @property
    def center_y(self):
        return self.bottom + (self.top - self.bottom) // 2

    @center_y.setter
    def center_y(self, value):
        y_diff = value - self.center_y
        self.move(0, y_diff)

    def move(self, x, y):
        self._top += y
        self._left += x

        for element, data in self._elements:
            element.top += y
            element.left += x

    # ---------- placement and refresh

    def changed(self):
        """Notify parent that this layout changed"""
        if self.parent:
            self.parent.changed()

    def refresh(self):
        for element in self:
            if isinstance(element, UILayout):
                element.refresh()
        self.place_elements()
        # self.refresh_background()

    @abstractmethod
    def place_elements(self):
        raise NotImplementedError()

    # ----------- Background
    # @property
    # def bg(self):
    #     return self._bg
    #
    # @bg.setter
    # def bg(self, value: UIElement):
    #     self._bg = value
    #     self.refresh_background()
    #
    # def refresh_background(self):
    #     if self.bg and len(self) > 0:
    #         self.bg.width = self.width
    #         self.bg.height = self.height
    #         self.bg.left = self.left
    #         self.bg.top = self.top

    def __iter__(self):
        yield from map(attrgetter('element'), self._elements)

    def __len__(self):
        return len(self._elements)
