from unittest.mock import Mock

import arcade

from arcade_gui import KEY_PRESS, KEY_RELEASE, MOUSE_PRESS, MOUSE_SCROLL, MOUSE_RELEASE, UIView


def test_added_ui_element_is_drawn():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_draw()

    assert ui_element.on_draw.called


def test_added_ui_element_is_updated():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_update(0)

    assert ui_element.on_update.called


def test_on_mouse_press_passes_an_event():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_mouse_press(1, 2, 3, 4)

    event, *_ = ui_element.on_event.call_args.args
    assert event.type == MOUSE_PRESS
    assert event.x == 1
    assert event.y == 2
    assert event.button == 3
    assert event.modifiers == 4


def test_on_mouse_release_passes_an_event():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_mouse_release(1, 2, 3, 4)

    event, *_ = ui_element.on_event.call_args.args
    assert event.type == MOUSE_RELEASE
    assert event.x == 1
    assert event.y == 2
    assert event.button == 3
    assert event.modifiers == 4


def test_on_mouse_scroll_passes_an_event():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_mouse_scroll(1, 2, 3, 4)

    event, *_ = ui_element.on_event.call_args.args
    assert event.type == MOUSE_SCROLL
    assert event.x == 1
    assert event.y == 2
    assert event.scroll_x == 3
    assert event.scroll_y == 4


def test_on_key_press_passes_an_event():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_key_press(arcade.key.ENTER, 0)

    event, *_ = ui_element.on_event.call_args.args
    assert event.type == KEY_PRESS
    assert event.symbol == arcade.key.ENTER


def test_on_key_release_passes_an_event():
    subject = UIView()
    ui_element = Mock()
    subject.add_ui_element(ui_element)

    subject.on_key_release(arcade.key.ENTER, 0)

    event, *_ = ui_element.on_event.call_args.args
    assert event.type == KEY_RELEASE
    assert event.symbol == arcade.key.ENTER
