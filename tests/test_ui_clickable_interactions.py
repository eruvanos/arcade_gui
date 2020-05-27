from uuid import uuid4

import PIL
import arcade
import pytest

from arcade_gui import UIClickable


class MockButton(UIClickable):
    on_hover_called = False
    on_unhover_called = False
    on_press_called = False
    on_release_called = False
    on_click_called = False

    def on_hover(self):
        super().on_hover()
        self.on_hover_called = True

    def on_unhover(self):
        super().on_unhover()
        self.on_unhover_called = True

    def on_press(self):
        super().on_press()
        self.on_press_called = True

    def on_release(self):
        super().on_release()
        self.on_release_called = True

    def on_click(self):
        super().on_click()
        self.on_click_called = True


@pytest.fixture()
def mock_button(view) -> MockButton:
    button = MockButton(view, center_x=50, center_y=50)

    button.normal_texture = arcade.Texture(image=PIL.Image.new("RGBA", (40, 40)), name=str(uuid4()))
    button.hover_texture = arcade.Texture(image=PIL.Image.new("RGBA", (40, 40)), name=str(uuid4()))
    button.press_texture = arcade.Texture(image=PIL.Image.new("RGBA", (40, 40)), name=str(uuid4()))
    button.focus_texture = arcade.Texture(image=PIL.Image.new("RGBA", (40, 40)), name=str(uuid4()))
    return button


def test_has_normal_state(mock_button):
    assert not mock_button.hovered
    assert not mock_button.pressed
    assert not mock_button.focused


def test_change_state_on_hover(mock_button):
    mock_button.on_hover()
    assert mock_button.hovered


def test_change_state_on_press(mock_button):
    mock_button.on_press()
    assert mock_button.pressed


def test_change_state_on_button(mock_button):
    mock_button.on_focus()
    assert mock_button.focused


def test_hover_point(mock_button):
    assert mock_button.hover_point(50, 50) is True
    assert mock_button.hover_point(30, 50) is True
    assert mock_button.hover_point(50, 30) is True
    assert mock_button.hover_point(0, 30) is False
    assert mock_button.hover_point(30, 0) is False


def test_uibutton_is_pressed(view, mock_button):
    view.add_ui_element(mock_button)

    view.click_and_hold(50, 50)

    assert mock_button.on_press_called
    assert not mock_button.on_click_called


def test_uibutton_clicked(view, mock_button):
    view.add_ui_element(mock_button)

    view.click(50, 50)

    assert mock_button.on_release
    assert mock_button.on_click_called


def test_uibutton_not_clicked_if_released_beside(view, mock_button):
    view.add_ui_element(mock_button)

    view.click_and_hold(50, 50)
    view.release(100, 100)

    assert not mock_button.on_click_called


def test_uibutton_send_custom_event(view, mock_button):
    view.add_ui_element(mock_button)

    view.click(50, 50)

    assert view.last_event.type == UIClickable.CLICKED
    assert view.last_event.ui_element == mock_button
