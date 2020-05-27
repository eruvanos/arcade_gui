import os
from typing import List

import pytest

import arcade_gui
from arcade_gui import UIClickable, UIView


class TestUIView(arcade_gui.UIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_history: List[arcade_gui.UIEvent] = []

    def click_and_hold(self, x: int, y: int):
        self.on_event(arcade_gui.UIEvent(
            arcade_gui.MOUSE_PRESS,
            x=x,
            y=y,
            button=1,
            modifier=0
        ))

    def release(self, x: int, y: int):
        self.on_event(arcade_gui.UIEvent(
            arcade_gui.MOUSE_RELEASE,
            x=x,
            y=y,
            button=1,
            modifier=0
        ))

    def click(self, x: int, y: int):
        self.click_and_hold(x, y)
        self.release(x, y)

    def on_event(self, event: arcade_gui.UIEvent):
        self.event_history.append(event)
        super().on_event(event)

    @property
    def last_event(self):
        return self.event_history[-1] if self.event_history else None


def T(name, *args):
    return pytest.param(*args, id=name)


class MockHolder(dict):
    """
    MockHolder, dict like object with property access
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class Env:
    def __init__(self, **kwargs):
        self.variables = kwargs
        self.old_vars = {}

    def __enter__(self):
        for key, value in self.variables.items():
            if key in os.environ:
                self.old_vars[key] = os.environ[key]

            os.environ[key] = value

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self.variables.keys():
            del os.environ[key]

        for key, value in self.old_vars.items():
            os.environ[key] = value


class MockButton(UIClickable):
    on_hover_called = False
    on_unhover_called = False
    on_press_called = False
    on_release_called = False
    on_click_called = False
    on_update_called = False
    on_focus_called = False
    on_unfocus_called = False

    def __init__(self, parent: UIView, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.event_history: List[arcade_gui.UIEvent] = []

    def on_event(self, event: arcade_gui.UIEvent):
        self.event_history.append(event)
        super().on_event(event)

    @property
    def last_event(self):
        return self.event_history[-1] if self.event_history else None

    def on_hover(self):
        super().on_hover()
        self.on_hover_called = True

    def on_unhover(self):
        super().on_unhover()
        self.on_unhover_called = True

    def on_press(self):
        super().on_press()
        self.on_press_called = True

    def on_release(self):
        super().on_release()
        self.on_release_called = True

    def on_click(self):
        super().on_click()
        self.on_click_called = True

    def on_focus(self):
        super().on_focus()
        self.on_focus_called = True

    def on_unfocus(self):
        super().on_unfocus()
        self.on_unfocus_called = True

    def on_update(self, delta_time: float = 1 / 60):
        super().on_update(delta_time)
        self.on_update_called = True


