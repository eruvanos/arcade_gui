from contextlib import ExitStack
from unittest.mock import patch

from pytest import fixture

from tests import TestUIView, MockHolder


@fixture
def view() -> TestUIView:
    return TestUIView()


@fixture()
def draw_commands():
    """
    Decorator

    Mocks all 'arcade.draw_...' methods and injects a holder with mocks
    """
    import arcade
    to_patch = [attr for attr in dir(arcade) if attr.startswith('draw_')]
    holder = MockHolder()

    with ExitStack() as stack:
        for method in to_patch:
            holder[method] = stack.enter_context(patch(f'arcade.{method}'))

        yield holder
