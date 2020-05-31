import pytest
from arcade.key import *

from arcade_gui import UIEvent, TEXT_INPUT, TEXT_MOTION
from arcade_gui.elements.inputbox import UIInputBox
from tests import T


def test_hover_point(view):
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


@pytest.mark.skip('This is hard to test, we would have to check the rendered texture, or mock the render calls')
def test_shows_cursor_if_focused(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Great UI'
    inputbox.cursor_index = 6
    view.add_ui_element(inputbox)

    # THEN
    # TODO somehow test that '|' is now in the inputbox.texture -.-
    # maybe have a image comparision


def test_set_cursor_behind_text_if_given_at_construction_time(draw_commands, view):
    inputbox = UIInputBox(
        text='arcade',
        center_x=30,
        center_y=30,
        width=40,
        height=40)

    # THEN
    assert inputbox.cursor_index == 7


def test_changes_text_on_text_input(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='a'))

    assert inputbox.text == 'Best aGame Lib!'
    assert inputbox.cursor_index == 6


def test_ignores_newline(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='\r'))

    assert inputbox.text == 'Best Game Lib!'
    assert inputbox.cursor_index == 5


def test_emits_event_on_enter(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_INPUT, text='\r'))

    assert view.last_event.type == UIInputBox.ENTER
    assert view.last_event.ui_element == inputbox


def test_changes_text_on_backspace(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_BACKSPACE))

    assert inputbox.text == 'BestGame Lib!'
    assert inputbox.cursor_index == 4


def test_changes_text_on_delete(draw_commands, view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=MOTION_DELETE))

    assert inputbox.text == 'Best ame Lib!'
    assert inputbox.cursor_index == 5


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
    inputbox.text = 'Best Game Lib!'
    inputbox.cursor_index = 5
    inputbox.on_focus()
    view.add_ui_element(inputbox)

    inputbox.on_event(UIEvent(TEXT_MOTION, motion=motion))

    assert inputbox.cursor_index == expected_index


def test_cursor_index_not_outside_text(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = 5

    assert inputbox.cursor_index == 4


def test_cursor_index_always_greater_equals_0(view):
    inputbox = UIInputBox(center_x=30, center_y=30, width=40, height=40)
    inputbox.text = 'love'
    inputbox.cursor_index = -1

    assert inputbox.cursor_index == 0
