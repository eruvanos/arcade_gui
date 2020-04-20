from unittest.mock import Mock

from arcade_gui import UIView, UIEvent, MOUSE_PRESS


def test_view_tracks_focused_element():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    focused = subject.focused_element

    assert focused is None


def test_click_on_element_makes_it_active():
    subject = UIView()
    ui_element = Mock()
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    subject.add_ui_element(ui_element)

    subject.on_event(UIEvent(MOUSE_PRESS, x=50, y=50, button=1, modifier=0))

    assert subject.focused_element is ui_element
    assert ui_element.on_focus.called


def test_click_beside_element_unfocuses():
    subject = UIView()
    ui_element = Mock()
    ui_element.hover_point.side_effect = lambda x, y: 20 <= x <= 80 and 20 <= y <= 80

    subject.add_ui_element(ui_element)
    subject.focused_element = ui_element

    subject.on_event(UIEvent(MOUSE_PRESS, x=100, y=100, button=1, modifier=0))

    assert subject.focused_element is None
    assert ui_element.on_unfocus.called
