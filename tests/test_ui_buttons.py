from unittest.mock import Mock

from arcade_gui import UIButton
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
    button.on_press.assert_called_once()
    button.on_click.assert_not_called()


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
    button.on_release.assert_called_once()
    button.on_click.assert_called_once()


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

    button.on_click.assert_not_called()


def test_uibutton_send_custom_event():
    view = TestUIView()
    button: UIButton = UIButton('hello world', center_x=50, center_y=50, width=40, height=40)
    view.add_ui_element(button)

    view.click(50, 50)

    assert view.last_event.type == UIButton.CLICKED
    assert view.last_event.ui_element == button
