from arcade_gui import UIEvent, MOUSE_PRESS
from tests import MockButton


def test_view_starts_without_focused_element(view):
    assert view.focused_element is None


def test_setting_focused_element_handles_focus(view, mock_button):
    view.add_ui_element(mock_button)

    view.focused_element = mock_button

    assert view.focused_element == mock_button
    assert mock_button.on_focus_called


def test_setting_focused_element_to_none_handles_unfocus(view, mock_button):
    view.add_ui_element(mock_button)

    view.focused_element = mock_button
    view.focused_element = None

    assert view.focused_element is None
    assert mock_button.on_unfocus_called


def test_setting_focus_to_other_element_handles_refocus(view, mock_button, mock_button2: MockButton):
    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button2)
    view.focused_element = mock_button

    # WHEN
    view.focused_element = mock_button2

    # THEN
    # old element unfocused
    assert mock_button.on_unfocus_called

    # New element focused
    assert view.focused_element == mock_button2
    assert mock_button2.on_focus_called
    assert not mock_button2.on_unfocus_called


def test_click_on_element_makes_it_active(view, mock_button):
    view.add_ui_element(mock_button)

    view.on_event(UIEvent(MOUSE_PRESS, x=50, y=50, button=1, modifier=0))

    assert view.focused_element is mock_button
    assert mock_button.on_focus_called


def test_click_beside_element_unfocuses(view, mock_button):
    view.add_ui_element(mock_button)
    view.focused_element = mock_button

    view.on_event(UIEvent(MOUSE_PRESS, x=100, y=100, button=1, modifier=0))

    assert view.focused_element is None
    assert mock_button.on_unfocus_called


def test_change_focus_to_different_element(view, mock_button: MockButton, mock_button2: MockButton):
    mock_button.center_x += 100

    view.add_ui_element(mock_button)
    view.add_ui_element(mock_button2)
    view.focused_element = mock_button

    # WHEN
    view.on_event(UIEvent(MOUSE_PRESS, x=50, y=50, button=1, modifier=0))

    # THEN
    assert view.focused_element is mock_button2
    assert mock_button.on_unfocus_called
    assert mock_button2.on_focus_called
