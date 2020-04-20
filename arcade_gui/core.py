from typing import List

import arcade
from arcade import View

from arcade_gui import MOUSE_PRESS, MOUSE_RELEASE, MOUSE_SCROLL, KEY_PRESS, KEY_RELEASE


class UIEvent:
    def __init__(self, type: str, **kwargs):
        self.type = type
        self.__dict__.update(**kwargs)


class UIElement:
    def on_event(self, event: UIEvent):
        pass

    def on_draw(self):
        pass

    def on_focus(self):
        """
        Callback if the element gets focused
        """
        pass

    def on_unfocus(self):
        """
        Callback if the element gets unfocused aka not focused any more
        """
        pass

    def on_update(self, dt: float):
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


class UIView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()  # Here happens a lot of stuff we don't need
        self.focused_element = None

        self._ui_elements: List[UIElement] = []

    def purge_ui_elements(self):
        self._ui_elements = []

    def add_ui_element(self, ui_element: UIElement):
        self._ui_elements.append(ui_element)

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
        for ui_element in self._ui_elements:
            ui_element.on_draw()

    def on_event(self, event: UIEvent):
        """
        Processes UIEvents, forward events to registered elements and manages focused element
        """
        for ui_element in self._ui_elements:
            if event.type == MOUSE_PRESS:
                if ui_element.hover_point(event.x, event.y):
                    ui_element.on_focus()
                    self.focused_element = ui_element

                elif ui_element is self.focused_element:
                    if self.focused_element:
                        self.focused_element.on_unfocus()
                    self.focused_element = None

            ui_element.on_event(event)

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
