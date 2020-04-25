from unittest.mock import Mock

from arcade_gui import UIView, UIEvent, UIElement
from arcade_gui.core import MOUSE_MOTION


def test_view_starts_without_hovered_element():
    assert UIView().hovered_element is None


def test_setting_hovered_element_to_None_handles_unhover():
    view = UIView()
    ui_element = Mock(spec=UIElement())
    view.add_ui_element(ui_element)

    view.hovered_element = ui_element
    view.hovered_element = None

    assert view.hovered_element is None
    ui_element.on_unhover.assert_called_once()


def test_setting_hovered_element_calls_on_hover():
    view = UIView()
    ui_element = Mock(spec=UIElement())
    view.add_ui_element(ui_element)

    view.hovered_element = ui_element

    assert view.hovered_element == ui_element
    ui_element.on_hover.assert_called_once()


def test_setting_hover_to_other_element_handles_rehover():
    view = UIView()
    ui_element1 = Mock(spec=UIElement())
    ui_element2 = Mock(spec=UIElement())
    view.add_ui_element(ui_element1)
    view.add_ui_element(ui_element2)
    view.hovered_element = ui_element1

    # WHEN
    view.hovered_element = ui_element2

    # THEN
    # old element unhovered
    ui_element1.on_unhover.assert_called_once()

    # New element hovered
    assert view.hovered_element == ui_element2
    ui_element2.on_hover.assert_called_once()
    ui_element2.on_unhover.assert_not_called()


def test_mouse_motion_over_element_makes_it_hovered():
    view = UIView()
    ui_element = Mock(spec=UIElement())
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    view.add_ui_element(ui_element)

    view.on_event(UIEvent(MOUSE_MOTION, x=50, y=50, dx=1, dy=1))

    assert view.hovered_element is ui_element
    ui_element.on_hover.assert_called_once()


def test_motion_out_of_element_unhoveres():
    view = UIView()
    ui_element = Mock(spec=UIElement())
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    view.add_ui_element(ui_element)
    view.hovered_element = ui_element

    view.on_event(UIEvent(MOUSE_MOTION, x=100, y=100, button=1, modifier=0))

    assert view.hovered_element is None
    ui_element.on_unhover.assert_called_once()


def test_change_hover_over_different_element():
    view = UIView()
    ui_element1 = Mock(spec=UIElement())
    ui_element2 = Mock(spec=UIElement())
    ui_element1.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80
    ui_element2.hover_point.side_effect = lambda x, y: 120 <= x <= 180 and 120 <= y <= 180

    view.add_ui_element(ui_element1)
    view.add_ui_element(ui_element2)
    view.hovered_element = ui_element1

    # WHEN
    view.on_event(UIEvent(MOUSE_MOTION, x=150, y=150, button=1, modifier=0))

    # THEN
    assert view.hovered_element is ui_element2
    ui_element1.on_unhover.assert_called_once()
    ui_element2.on_hover.assert_called_once()
