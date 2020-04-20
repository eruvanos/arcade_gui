from unittest.mock import Mock

from arcade_gui.button import UIButton
from tests import TestUIView


def test_hover_point():
    button = UIButton(
        'hello world',
        center_x=50,
        center_y=50,
        width=40,
        height=40,
    )

    assert button.hover_point(50, 50) is True
    assert button.hover_point(30, 50) is True
    assert button.hover_point(50, 30) is True
    assert button.hover_point(0, 30) is False
    assert button.hover_point(30, 0) is False


def test_uibutton_is_pressed():
    view = TestUIView()
    button: UIButton = UIButton(
        'hello world',
        center_x=50,
        center_y=50,
        width=40,
        height=40,
    )
    button.on_press = Mock()
    button.on_click = Mock()
    view.add_ui_element(button)

    view.click_and_hold(50, 50)

    assert button.pressed
    assert button.on_press.called
    assert not button.on_click.called


def test_uibutton_clicked():
    view = TestUIView()
    button: UIButton = UIButton(
        'hello world',
        center_x=50,
        center_y=50,
        width=40,
        height=40,
    )
    button.on_press = Mock()
    button.on_release = Mock()
    button.on_click = Mock()
    view.add_ui_element(button)

    view.click(50, 50)

    assert not button.pressed
    assert button.on_release.called
    assert button.on_click.called


def test_uibutton_not_clicked_if_released_beside():
    view = TestUIView()
    button: UIButton = UIButton(
        'hello world',
        center_x=50,
        center_y=50,
        width=40,
        height=40,
    )
    button.on_press = Mock()
    button.on_release = Mock()
    button.on_click = Mock()
    view.add_ui_element(button)

    view.click_and_hold(50, 50)
    view.release(100, 100)

    assert not button.on_click.called
