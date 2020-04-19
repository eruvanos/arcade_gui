__version__ = '0.1.0'

from typing import List

from arcade import View

MOUSE_PRESS = 'MOUSE_PRESS'
MOUSE_RELEASE = 'MOUSE_RELEASE'
MOUSE_SCROLL = 'MOUSE_SCROLL'
KEY_PRESS = 'KEY_PRESS'
KEY_RELEASE = 'KEY_RELEASE'


class UIEvent:
    def __init__(self, type: str, **kwargs):
        self.type = type
        self.__dict__.update(**kwargs)


class UIElement:
    def on_event(self, event: UIEvent):
        pass

    def on_draw(self):
        pass

    def on_update(self, dt: float):
        pass


class UIView(View):
    def __init__(self, *args, **kwargs):
        super().__init__()  # Here happens a lot of stuff we don't need

        self._ui_elements: List[UIElement] = []

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
        for ui_element in self._ui_elements:
            ui_element.on_draw()

    def on_event(self, event: UIEvent):
        for ui_element in self._ui_elements:
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
