from contextlib import ExitStack
from unittest.mock import patch
from uuid import uuid4

import PIL
import arcade
import pytest
from pytest import fixture

from tests import TestUIView, MockHolder, MockButton


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


@pytest.fixture()
def mock_button() -> MockButton:
    return MockButton(center_x=50, center_y=50, width=40, height=40)


# provide same fixture twice, in case we need a second button
mock_button2 = mock_button
