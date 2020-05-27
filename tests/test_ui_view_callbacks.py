from unittest.mock import patch

import arcade
from arcade.key import MOTION_UP

from arcade_gui import MOUSE_PRESS, MOUSE_RELEASE, MOUSE_SCROLL, KEY_PRESS, KEY_RELEASE, TEXT_MOTION_SELECTION
from arcade_gui import TEXT_INPUT, TEXT_MOTION
from arcade_gui.core import MOUSE_MOTION
from tests import MockButton


def test_added_ui_element_is_drawn(view, mock_button):
    view.add_ui_element(mock_button)

    assert mock_button in view._ui_elements


def test_added_ui_element_is_updated(view, mock_button: MockButton):
    view.add_ui_element(mock_button)

    view.on_update(0)

    assert mock_button.on_update_called


def test_on_mouse_press_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)

    view.on_mouse_press(1, 2, 3, 4)

    event = mock_button.last_event
    assert event.type == MOUSE_PRESS
    assert event.x == 1
    assert event.y == 2
    assert event.button == 3
    assert event.modifiers == 4


def test_on_mouse_release_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)

    view.on_mouse_release(1, 2, 3, 4)

    event = mock_button.last_event
    assert event.type == MOUSE_RELEASE
    assert event.x == 1
    assert event.y == 2
    assert event.button == 3
    assert event.modifiers == 4


def test_on_mouse_scroll_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_mouse_scroll(1, 2, 3, 4)

    event = mock_button.last_event
    assert event.type == MOUSE_SCROLL
    assert event.x == 1
    assert event.y == 2
    assert event.scroll_x == 3
    assert event.scroll_y == 4


def test_on_mouse_motion_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_mouse_motion(1, 2, 3, 4)

    event = mock_button.last_event
    assert event.type == MOUSE_MOTION
    assert event.x == 1
    assert event.y == 2
    assert event.dx == 3
    assert event.dy == 4


def test_on_key_press_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_key_press(arcade.key.ENTER, 0)

    event = mock_button.last_event
    assert event.type == KEY_PRESS
    assert event.symbol == arcade.key.ENTER


def test_on_key_release_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_key_release(arcade.key.ENTER, 0)

    event = mock_button.last_event
    assert event.type == KEY_RELEASE
    assert event.symbol == arcade.key.ENTER


def test_on_text_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_text('a')

    event = mock_button.last_event
    assert event.type == TEXT_INPUT
    assert event.text == 'a'


def test_on_text_motion_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_text_motion(MOTION_UP)

    event = mock_button.last_event
    assert event.type == TEXT_MOTION
    assert event.motion == MOTION_UP


def test_on_text_motion_selection_passes_an_event(view, mock_button):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button)

    view.on_text_motion_selection(MOTION_UP)

    event = mock_button.last_event
    assert event.type == TEXT_MOTION_SELECTION
    assert event.selection == MOTION_UP
