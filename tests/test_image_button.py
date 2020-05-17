from unittest.mock import call, Mock

import arcade
import pytest
from arcade import Texture

from arcade_gui.buttons.image_button import UIImageButton


@pytest.fixture()
def button(view) -> UIImageButton:
    normal_texture = Mock(spec=Texture, width=10, height=10)
    hovered_texture = Mock(spec=Texture, width=20, height=20)
    pressed_texture = Mock(spec=Texture, width=20, height=20)

    b = UIImageButton(
        center_x=30,
        center_y=40,
        normal_texture=normal_texture,
        hovered_texture=hovered_texture,
        pressed_texture=pressed_texture,
    )
    view.add_ui_element(b)
    return b


def test_shows_text(draw_commands, button):
    button.text = 'Start Game'

    button.on_draw()

    assert draw_commands.draw_text.call_args == call(
        'Start Game',
        30,
        40,
        arcade.color.BLACK,
        width=button.width,
        font_size=20,
        align='center',
        anchor_x="center", anchor_y="center"
    )


def test_shows_normal_texture_using_normal_texture_size(draw_commands, button):
    button.on_draw()

    assert draw_commands.draw_texture_rectangle.call_args == call(
        30,
        40,
        button.normal_texture.width,
        button.normal_texture.height,
        button.normal_texture
    )


def test_on_hover_shows_hover_texture_using_normal_texture_size(draw_commands, button):
    button.on_hover()
    button.on_draw()

    assert draw_commands.draw_texture_rectangle.call_args == call(
        30,
        40,
        button.normal_texture.width,
        button.normal_texture.height,
        button.hovered_texture
    )


def test_on_press_shows_pressed_texture_using_normal_texture_size(draw_commands, button):
    button.on_press()
    button.on_draw()

    assert draw_commands.draw_texture_rectangle.call_args == call(
        30,
        40,
        button.normal_texture.width,
        button.normal_texture.height,
        button.pressed_texture
    )
