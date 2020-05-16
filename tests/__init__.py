import os
from typing import List

import pytest

import arcade_gui


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
