from arcade_gui import UIView, UIEvent
from arcade_gui.core import MOUSE_MOTION
from tests import MockButton


def test_view_starts_without_hovered_element():
    assert UIView().hovered_element is None


def test_setting_hovered_element_to_None_handles_unhover(view, mock_button):
    view.add_ui_element(mock_button)

    view.hovered_element = mock_button
    view.hovered_element = None

    assert view.hovered_element is None
    assert mock_button.on_unhover_called


def test_setting_hovered_element_calls_on_hover(view, mock_button):
    view.add_ui_element(mock_button)

    view.hovered_element = mock_button

    assert view.hovered_element == mock_button
    assert mock_button.on_hover_called


def test_setting_hover_to_other_element_handles_rehover(view, mock_button, mock_button2: MockButton):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button2)
    view.hovered_element = mock_button

    # WHEN
    view.hovered_element = mock_button2

    # THEN
    # old element unhovered
    assert mock_button.on_unhover_called

    # New element hovered
    assert view.hovered_element == mock_button2
    assert mock_button2.on_hover_called
    assert not mock_button2.on_unhover_called


def test_mouse_motion_over_element_makes_it_hovered(view, mock_button):
    view.add_ui_element(mock_button)

    view.on_event(UIEvent(MOUSE_MOTION, x=50, y=50, dx=1, dy=1))

    assert view.hovered_element is mock_button
    assert mock_button.on_hover_called


def test_motion_out_of_element_unhoveres(view, mock_button):
    view.add_ui_element(mock_button)
    view.hovered_element = mock_button

    view.on_event(UIEvent(MOUSE_MOTION, x=100, y=100, button=1, modifier=0))

    assert view.hovered_element is None
    assert mock_button.on_unhover_called


def test_change_hover_over_different_element(view, mock_button, mock_button2: MockButton):
    mock_button.center_x += 100

    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button2)
    view.hovered_element = mock_button

    # WHEN
    view.on_event(UIEvent(MOUSE_MOTION, x=50, y=50, button=1, modifier=0))

    # THEN
    assert view.hovered_element is mock_button2
    assert mock_button.on_unhover_called
    assert mock_button2.on_hover_called
