from contextlib import ExitStack
from unittest.mock import patch

import pytest

import arcade_gui


class TestUIView(arcade_gui.UIView):

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
        super().on_event(event)


def T(name, *args):
    return pytest.param(*args, id=name)


class MockHolder(dict):
    """
    MockHolder, dict like object with property access
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def patch_draw_commands(f):
    """
    Decorator

    Mocks all 'arcade.draw_...' methods and injects a holder with mocks
    """
    import arcade

    to_patch = [attr for attr in dir(arcade) if attr.startswith('draw_')]
    holder = MockHolder()

    def wrapper(*args, **kwargs):
        with ExitStack() as stack:
            for method in to_patch:
                holder[method] = stack.enter_context(patch(f'arcade.{method}'))
            return f(holder, *args, **kwargs)

    return wrapper
