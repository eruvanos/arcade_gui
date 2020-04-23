import os
from unittest.mock import patch, ANY, call

import arcade
import pytest
from arcade.key import *

from arcade_gui import UIEvent, TEXT_INPUT, TEXT_MOTION
from arcade_gui.inputbox import UIInputBox
from tests import TestUIView, T, patch_draw_commands


def test_hover_point():
    inputbox = UIInputBox(
        x=30,
        y=30,
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


def test_highlight_on_focus():
    view = TestUIView()
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    # WHEN
    view.click(50, 50)

    # THEN
    assert inputbox.text_display.highlighted


def test_normal_on_unfocus():
    view = TestUIView()
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    view.add_ui_element(inputbox)

    # WHEN
    view.click(50, 50)
    view.click(150, 50)

    # THEN
    assert not inputbox.text_display.highlighted


@patch_draw_commands
def test_draws_border(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)

    inputbox.on_draw()

    draws.draw_rectangle_outline.assert_called_once()


@patch_draw_commands
def test_shows_cursor_if_highlighted(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Great UI'
    inputbox.cursor_index = 6

    # WHEN
    inputbox.on_draw()

    # THEN
    text, *_ = draws.draw_text.call_args.args
    assert text == 'Great |UI'


@patch_draw_commands
def test_dont_render_text_if_empty(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)

    # WHEN
    inputbox.on_draw()

    # THEN
    draws.draw_text.assert_not_called()


@patch_draw_commands
def test_render_normal_text(draws):
    expected_font_size = 42
    expected_text = 'Great UI'
    inputbox = UIInputBox(x=30, y=30, width=40, height=40, font_size=expected_font_size)
    inputbox.text = expected_text

    # WHEN
    inputbox.on_draw()

    # THEN
    assert draws.draw_text.call_args == call(
        expected_text,
        ANY,
        ANY,
        arcade.color.BLACK,
        font_size=expected_font_size,
        anchor_y='center',
        font_name=('Calibri', 'Arial')
    )


@patch_draw_commands
def test_changes_text_on_text_input(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5

    inputbox.on_event(UIEvent(TEXT_INPUT, text='a'))
    inputbox.on_draw()

    text, *_ = draws.draw_text.call_args.args
    assert text == 'Best a|Game Lib!'


@patch_draw_commands
def test_ignores_newline(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5

    inputbox.on_event(UIEvent(TEXT_INPUT, text='\r'))
    inputbox.on_draw()

    text, *_ = draws.draw_text.call_args.args
    assert text == 'Best |Game Lib!'


@patch_draw_commands
def test_changes_text_on_backspace(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_BACKSPACE))
    inputbox.on_draw()

    text, *_ = draws.draw_text.call_args.args
    assert text == 'Best|Game Lib!'


@patch_draw_commands
def test_changes_text_on_delete(draws):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_DELETE))
    inputbox.on_draw()

    text, *_ = draws.draw_text.call_args.args
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
def test_changes_cursor_on_text_motion(motion, expected_index):
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text_display.highlighted = True
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=motion))

    assert inputbox.cursor_index == expected_index


def test_cursor_in_sync():
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text = 'awesome'
    inputbox.cursor_index = 5

    assert inputbox.text_display.cursor_index == 5
    assert inputbox.text_adapter.cursor_index == 5


def test_cursor_index_not_outside_text():
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = 5

    assert inputbox.cursor_index == 4


def test_cursor_index_always_greater_equals_0():
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = -1

    assert inputbox.cursor_index == 0


def test_text_in_sync():
    inputbox = UIInputBox(x=30, y=30, width=40, height=40)
    inputbox.text = 'Nice Games!'

    assert inputbox.text_display.text == 'Nice Games!'
    assert inputbox.text_adapter.text == 'Nice Games!'
