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

    def register_handlers(self):
        """
        Registers handler functions (`on_...`) to :py:attr:`arcade.gui.UIElement`
        """
        # self.window.push_handlers(self) # Not as explicit as following
        self.window.push_handlers(
            self.on_resize,
            self.on_update,
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
                 **kwargs):
        super().__init__()
        self.draw_border = draw_border
        self._parent: Optional[UILayoutParent] = parent

        self._elements: List[PackedElement] = []
        self._layer = SpriteList()
        self._child_layouts = []

        # own position
        self._top = 0
        self._left = 0

        self._width = 0
        self._height = 0

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
        self._layer.draw()
        self._layer.draw_hit_boxes(arcade.color.LIGHT_RED_OCHRE, 2)
        for child in self._child_layouts:
            child.draw()

    # def update_size_hint(self):
    #     raise NotImplementedError()
    #
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
