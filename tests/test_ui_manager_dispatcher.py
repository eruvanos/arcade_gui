from unittest.mock import Mock, call

from arcade_gui import UIManager


def test_handler_pushed():
    window = Mock()

    msg = UIManager(window)

    window.assert_has_calls([
        call.push_handlers(msg.on_update),
        call.push_handlers(msg.on_draw),
        call.push_handlers(msg.on_mouse_press),
        call.push_handlers(msg.on_mouse_release),
        call.push_handlers(msg.on_mouse_scroll),
        call.push_handlers(msg.on_mouse_motion),
        call.push_handlers(msg.on_key_press),
        call.push_handlers(msg.on_key_release),
        call.push_handlers(msg.on_text),
        call.push_handlers(msg.on_text_motion),
        call.push_handlers(msg.on_text_motion_selection),
    ])
