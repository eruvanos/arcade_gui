from unittest.mock import Mock

from arcade_gui import UIView, UIEvent, MOUSE_PRESS, UIElement


def test_view_starts_without_focused_element():
    assert UIView().focused_element is None


def test_setting_focused_element_handles_focus():
    view = UIView()
    ui_element = Mock(spec=UIElement())
    view.add_ui_element(ui_element)

    view.focused_element = ui_element

    assert view.focused_element == ui_element
    ui_element.on_focus.assert_called_once()


def test_setting_focused_element_to_none_handles_unfocus():
    view = UIView()
    ui_element = Mock()
    view.add_ui_element(ui_element)

    view.focused_element = ui_element
    view.focused_element = None

    assert view.focused_element is None
    ui_element.on_unfocus.assert_called_once()


def test_setting_focus_to_other_element_handles_refocus():
    view = UIView()
    ui_element1 = Mock()
    ui_element2 = Mock()
    view.add_ui_element(ui_element1)
    view.add_ui_element(ui_element2)
    view.focused_element = ui_element1

    # WHEN
    view.focused_element = ui_element2

    # THEN
    # old element unfocused
    ui_element1.on_unfocus.assert_called_once()

    # New element focused
    assert view.focused_element == ui_element2
    ui_element2.on_focus.assert_called_once()
    ui_element2.on_unfocus.assert_not_called()


def test_click_on_element_makes_it_active():
    view = UIView()
    ui_element = Mock()
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    view.add_ui_element(ui_element)

    view.on_event(UIEvent(MOUSE_PRESS, x=50, y=50, button=1, modifier=0))

    assert view.focused_element is ui_element
    ui_element.on_focus.assert_called_once()


def test_click_beside_element_unfocuses():
    view = UIView()
    ui_element = Mock()
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    view.add_ui_element(ui_element)
    view.focused_element = ui_element

    view.on_event(UIEvent(MOUSE_PRESS, x=100, y=100, button=1, modifier=0))

    assert view.focused_element is None
    ui_element.on_unfocus.assert_called_once()


def test_change_focus_to_different_element():
    view = UIView()
    ui_element1 = Mock()
    ui_element2 = Mock()
    ui_element1.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80
    ui_element2.hover_point.side_effect = lambda x, y: 120 <= x <= 180 and 120 <= y <= 180

    view.add_ui_element(ui_element1)
    view.add_ui_element(ui_element2)
    view.focused_element = ui_element1

    # WHEN
    view.on_event(UIEvent(MOUSE_PRESS, x=150, y=150, button=1, modifier=0))

    # THEN
    assert view.focused_element is ui_element2
    ui_element1.on_unfocus.assert_called_once()
    ui_element2.on_focus.assert_called_once()
