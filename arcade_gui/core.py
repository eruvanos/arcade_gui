from typing import Dict, Optional

import arcade
from arcade import SpriteList

import arcade_gui
from arcade_gui.ui_style import UIStyle

MOUSE_PRESS = 'MOUSE_PRESS'
MOUSE_RELEASE = 'MOUSE_RELEASE'
MOUSE_SCROLL = 'MOUSE_SCROLL'
MOUSE_MOTION = 'MOUSE_MOTION'
KEY_PRESS = 'KEY_PRESS'
KEY_RELEASE = 'KEY_RELEASE'

TEXT_INPUT = 'TEXT_INPUT'
TEXT_MOTION = 'TEXT_MOTION'
TEXT_MOTION_SELECTION = 'TEXT_MOTION_SELECTION'


class UIEvent:
    def __init__(self, type: str, **kwargs):
        self.type = type
        self.__dict__.update(**kwargs)

        self._repr_keys = tuple(kwargs.keys())

    def __str__(self):
        return ' '.join([f'{self.type} ', *[f'{key}={getattr(self, key)}' for key in self._repr_keys]])


class Styled:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style_classes = ['globals']
        self._style = {}

    def set_style_attrs(self, **kwargs):
        """
        Sets a custom style attribute for this UIElement

        For a color the value should be formatted like 'BLACK', '42,42,42', '2A2A2A'

        :param kwargs: key-value pairs
        """
        for key, value in kwargs.items():
            if value is None:
                if key in self._style:
                    del self._style[key]
            else:
                self._style[key] = value

    def get_style_attr(self, key, default=None):
        return self._style.get(key, default)


class UIElement(Styled, arcade.Sprite):
    def __init__(self,
                 center_x=0, center_y=0,
                 id=None,
                 **kwargs):
        super().__init__()
        self.id = id
        self.view = None

        # what do we need to be a proper sprite
        # self.texture <- subclass
        # self.width/height <- subclass
        self.center_x = center_x
        self.center_y = center_y

    def parent_style(self) -> UIStyle:
        return self.view.style

    def find_color(self, param):
        # TODO would be better to parse the values on load and just return the values, instead of find_xyz
        parent_style = self.parent_style()
        return parent_style.get_color(self, param)

    def on_event(self, event: UIEvent):
        pass

    def on_focus(self):
        """
        Callback if the element gets focused
        """
        pass

    def on_unfocus(self):
        """
        Callback if the element gets unfocused aka is not focused any more
        """
        pass

    def on_hover(self):
        """
        Callback if the element gets hovered
        """
        pass

    def on_unhover(self):
        """
        Callback if the element gets unhovered aka is not focused any more
        """
        pass

    def on_update(self, delta_time: float = 1 / 60):
        pass

    def hover_point(self, hover_x: float, hover_y: float) -> bool:
        """
        Test if a given point counts as 'hovering' this UI element. Normally that is a
        straightforward matter of seeing if a point is inside the rectangle. Occasionally it
        will also check if we are in a wider zone around a UI element once it is already active,
        this makes it easier to move scroll bars and the like.

        :param hover_x: The x (horizontal) position of the point.
        :param hover_y: The y (vertical) position of the point.

        :return: Returns True if we are hovering this element.

        """
        return False


class UIException(Exception):
    pass


class UIView(arcade.View):
    def __init__(self, *args, **kwargs):
        super().__init__()  # Here happens a lot of stuff we don't need
        self._focused_element: Optional[UIElement] = None
        self._hovered_element: Optional[UIElement] = None

        self._ui_elements: SpriteList[UIElement] = SpriteList(use_spatial_hash=True)
        self._id_cache: Dict[str, UIElement] = {}

        self.style = UIStyle({})
        self.style.load(arcade_gui.resources.path('style/default.yml'))

    @property
    def focused_element(self):
        return self._focused_element

    @focused_element.setter
    def focused_element(self, new_focus: UIElement):

        if self._focused_element is not None:
            self._focused_element.on_unfocus()
            self._focused_element = None

        if new_focus is not None:            new_focus.on_focus()

        self._focused_element = new_focus

    @property
    def hovered_element(self):
        return self._hovered_element

    @hovered_element.setter
    def hovered_element(self, new_hover: UIElement):
        if self._hovered_element is not None:
            self._hovered_element.on_unhover()
            self._hovered_element = None

        if new_hover is not None:
            new_hover.on_hover()

        self._hovered_element = new_hover

    def purge_ui_elements(self):
        self._ui_elements = SpriteList()
        self._id_cache = {}

    def add_ui_element(self, ui_element: UIElement):
        if not hasattr(ui_element, 'id'):
            raise UIException('UIElement seems not to be properly setup, please check if you'
                              ' overwrite the constructor and forgot "super().__init__(**kwargs)"')

        ui_element.view = self
        self._ui_elements.append(ui_element)

        # Add elements with id to lookup
        if ui_element.id is not None:
            if ui_element.id in self._id_cache:
                raise UIException(f'duplicate id "{ui_element.id}"')

            self._id_cache[ui_element.id] = ui_element

    def update(self, delta_time: float):
        """
        Deprecated, use on_update
        """
        pass

    def on_update(self, delta_time: float):
        for ui_element in self._ui_elements:
            ui_element.on_update(delta_time)

    def on_draw(self):
        """
        Renders ui elements, already calls `arcade.start_render()`
        :return:
        """
        arcade.start_render()
        self._ui_elements.draw()

    def on_event(self, event: UIEvent):
        """
        Processes UIEvents, forward events to registered elements and manages focused element
        """
        for ui_element in self._ui_elements:
            if event.type == MOUSE_PRESS:
                if ui_element.hover_point(event.x, event.y):
                    self.focused_element = ui_element

                elif ui_element is self.focused_element:
                    # TODO does this work like expected?
                    self.focused_element = None

            if event.type == MOUSE_MOTION:
                if ui_element.hover_point(event.x, event.y):
                    self.hovered_element = ui_element

                elif ui_element is self.hovered_element:
                    self.hovered_element = None

            ui_element.on_event(event)

    def find_by_id(self, ui_element_id: str) -> Optional[UIElement]:
        return self._id_cache.get(ui_element_id)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        self.on_event(UIEvent(MOUSE_PRESS, x=x, y=y, button=button, modifiers=modifiers))

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.on_event(UIEvent(MOUSE_RELEASE, x=x, y=y, button=button, modifiers=modifiers))

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.on_event(UIEvent(MOUSE_SCROLL,
                              x=x,
                              y=y,
                              scroll_x=scroll_x,
                              scroll_y=scroll_y,
                              ))

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        super().on_mouse_motion(x, y, dx, dy)
        self.on_event(UIEvent(MOUSE_MOTION,
                              x=x,
                              y=y,
                              dx=dx,
                              dy=dy,
                              ))

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)
        self.on_event(UIEvent(KEY_PRESS,
                              symbol=symbol,
                              modifiers=modifiers
                              ))

    def on_key_release(self, symbol: int, modifiers: int):
        super().on_key_release(symbol, modifiers)
        self.on_event(UIEvent(KEY_RELEASE,
                              symbol=symbol,
                              modifiers=modifiers
                              ))

    def on_text(self, text):
        self.on_event(UIEvent(TEXT_INPUT,
                              text=text,
                              ))

    def on_text_motion(self, motion):
        self.on_event(UIEvent(TEXT_MOTION,
                              motion=motion,
                              ))

    def on_text_motion_selection(self, selection):
        self.on_event(UIEvent(TEXT_MOTION_SELECTION,
                              selection=selection,
                              ))
