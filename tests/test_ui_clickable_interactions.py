from arcade_gui import UIClickable


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


def test_change_state_on_focus(mock_button):
    mock_button.on_focus()
    assert mock_button.focused


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
