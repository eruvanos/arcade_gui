import pytest

from arcade_gui import UIButton


class MockButton(UIButton):
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
def mock_button() -> MockButton:
    return MockButton(
        'hello world',
        center_x=50,
        center_y=50,
        width=40,
        height=40,
    )


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

    assert view.last_event.type == UIButton.CLICKED
    assert view.last_event.ui_element == mock_button
