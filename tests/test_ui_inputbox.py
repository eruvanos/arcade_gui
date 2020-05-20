from unittest.mock import ANY, call

import arcade
import pytest
from arcade.key import *

from arcade_gui import UIEvent, TEXT_INPUT, TEXT_MOTION
from arcade_gui.elements.inputbox import UIInputBox
from tests import T


def test_hover_point():
    inputbox = UIInputBox(
        center_x=30,
        center_y=30,
        width=40,
        height=40,
    )

    # CENTER
    assert inputbox.hover_point(30, 30) is True
    # LEFT
    assert inputbox.hover_point(30, 40) is True
    assert inputbox.hover_point(9, 40) is False
    # TOP
    assert inputbox.hover_point(40, 50) is True
    assert inputbox.hover_point(40, 51) is False

    # RIGHT
    assert inputbox.hover_point(50, 40) is True
    assert inputbox.hover_point(51, 40) is False

    # BOTTOM
    assert inputbox.hover_point(40, 30) is True
    assert inputbox.hover_point(40, 9) is False


def test_highlight_on_focus(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    # WHEN
    view.click(50, 50)

    # THEN
    assert inputbox.text_display.highlighted


def test_normal_on_unfocus(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    # WHEN
    view.click(50, 50)
    view.click(150, 50)

    # THEN
    assert not inputbox.text_display.highlighted


def test_draws_border(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    inputbox.on_draw()

    draw_commands.draw_rectangle_outline.assert_called_once()


def test_shows_cursor_if_highlighted(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Great UI'
    inputbox.cursor_index = 6
    view.add_ui_element(inputbox)

    # WHEN
    inputbox.on_draw()

    # THEN
    text = draw_commands.draw_text.call_args[0][0]
    assert text == 'Great |UI'


def test_dont_render_text_if_empty(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    # WHEN
    inputbox.on_draw()

    # THEN
    draw_commands.draw_text.assert_not_called()


def test_render_normal_text(draw_commands, view):
    expected_font_size = 42
    expected_text = 'Great UI'
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40, font_size=expected_font_size)
    inputbox.text = expected_text
    view.add_ui_element(inputbox)

    # WHEN
    inputbox.on_draw()

    # THEN
    assert draw_commands.draw_text.call_args == call(
        expected_text,
        ANY,
        ANY,
        arcade.color.BLACK,
        font_size=expected_font_size,
        anchor_y='center',
        font_name=('Calibri', 'Arial')
    )


def test_changes_text_on_text_input(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='a'))
    inputbox.on_draw()

    text = draw_commands.draw_text.call_args[0][0]
    assert text == 'Best a|Game Lib!'


def test_ignores_newline(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='\r'))
    inputbox.on_draw()

    text = draw_commands.draw_text.call_args[0][0]
    assert text == 'Best |Game Lib!'


def test_emits_event_on_enter(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='\r'))

    assert view.last_event.type == UIInputBox.ENTER
    assert view.last_event.ui_element == inputbox


def test_changes_text_on_backspace(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_BACKSPACE))
    inputbox.on_draw()

    text = draw_commands.draw_text.call_args[0][0]
    assert text == 'Best|Game Lib!'


def test_changes_text_on_delete(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_DELETE))
    inputbox.on_draw()

    text = draw_commands.draw_text.call_args[0][0]
    assert text == 'Best |ame Lib!'


@pytest.mark.parametrize(
    'motion,expected_index',
    [
        # Test against 'Best |Game Lib!'
        T('MOTION_UP', MOTION_UP, 0),
        T('MOTION_RIGHT', MOTION_RIGHT, 6),
        T('MOTION_DOWN', MOTION_DOWN, 14),
        T('MOTION_LEFT', MOTION_LEFT, 4),
        # T('MOTION_NEXT_WORD', MOTION_NEXT_WORD, 5),
        # T('MOTION_PREVIOUS_WORD', MOTION_PREVIOUS_WORD, 5),
        T('MOTION_BEGINNING_OF_LINE', MOTION_BEGINNING_OF_LINE, 0),
        T('MOTION_END_OF_LINE', MOTION_END_OF_LINE, 14),
        T('MOTION_NEXT_PAGE', MOTION_NEXT_PAGE, 14),
        T('MOTION_PREVIOUS_PAGE', MOTION_PREVIOUS_PAGE, 0),
        T('MOTION_BEGINNING_OF_FILE', MOTION_BEGINNING_OF_FILE, 0),
        T('MOTION_END_OF_FILE', MOTION_END_OF_FILE, 14),
        T('MOTION_BACKSPACE', MOTION_BACKSPACE, 4),
        T('MOTION_DELETE', MOTION_DELETE, 5),
    ]
)
def test_changes_cursor_on_text_motion(motion, expected_index, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=motion))

    assert inputbox.cursor_index == expected_index


def test_cursor_in_sync():
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'awesome'
    inputbox.cursor_index = 5

    assert inputbox.text_display.cursor_index == 5
    assert inputbox.text_adapter.cursor_index == 5


def test_cursor_index_not_outside_text():
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = 5

    assert inputbox.cursor_index == 4


def test_cursor_index_always_greater_equals_0():
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = -1

    assert inputbox.cursor_index == 0


def test_text_in_sync():
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Nice Games!'

    assert inputbox.text_display.text == 'Nice Games!'
    assert inputbox.text_adapter.text == 'Nice Games!'
