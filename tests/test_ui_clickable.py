import arcade
import pytest

import arcade_gui
from arcade_gui import UIClickable


@pytest.fixture()
def button(view) -> UIClickable:
    normal_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
    hover_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
    focus_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))
    press_texture = arcade.load_texture(arcade_gui.resources('basic_ui_pack/red/red_button00.png'))

    b = UIClickable(
        view,
        center_x=30,
        center_y=40,
    )
    b.normal_texture = normal_texture
    b.hover_texture = hover_texture
    b.press_texture = press_texture
    b.focus_texture = focus_texture

    view.add_ui_element(b)
    return b


def test_shows_normal_texture(button):
    assert button.texture == button.normal_texture


def test_shows_hover_texture(button):
    button.on_hover()
    assert button.texture == button.hover_texture


def test_shows_press_texture(button):
    button.on_press()
    assert button.texture == button.press_texture


def test_shows_focus_texture(button):
    button.on_focus()
    assert button.texture == button.focus_texture