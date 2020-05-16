import arcade

from arcade_gui import FlatButton, GhostFlatButton, UI3DButton
from arcade_gui.ui_style import UIStyle, parse_color


def test_view_loads_default_style(view):
    assert view.style is not None


def test_ui_element_provides_ui_style_from_parent(view):
    button = FlatButton('Love snakes.', 100, 100, 100, 30)

    view.add_ui_element(button)

    assert button.parent_style() == view.style


def test_style_returns_property_for_ui_elements(shared_datadir, view):
    style = UIStyle({
        'flatbutton': {'normal_color': 'RED'},
        'ghostflatbutton': {'normal_color': 'BLUE'},
    })
    flat = FlatButton('Love snakes.', 100, 100, 100, 30)
    ghost = GhostFlatButton('Love snakes.', 100, 100, 100, 30)

    assert style.get_color(flat, 'normal_color') == arcade.color.RED
    assert style.get_color(ghost, 'normal_color') == arcade.color.BLUE


def test_style_returns_property_for_custom_ui_element(shared_datadir, view):
    class MyButton(FlatButton):
        """Custom button, which should use style attributes of FlatButton"""
        pass

    style = UIStyle({
        'flatbutton': {'normal_color': 'RED'},
    })

    flat = MyButton('Love snakes.', 100, 100, 100, 30)

    assert style.get_color(flat, 'normal_color') == arcade.color.RED


def test_style_returns_none_for_unknown_ui_element_class(shared_datadir, view):
    style = UIStyle({
        'flatbutton': {'normal_color': 'RED'},
    })
    button = UI3DButton('Love snakes.', 100, 100, 100, 30)

    assert style.get_color(button, 'normal_color') is None


def test_parse_rgb_values():
    rgb = parse_color('0,0,0')
    assert rgb == (0, 0, 0)


def test_parse_rgb_values_with_space():
    rgb = parse_color('0, 0, 0')
    assert rgb == (0, 0, 0)


def test_parse_hex_value():
    rgb = parse_color('ffffff')
    assert rgb == (255, 255, 255)


def test_parse_arcade_color():
    rgb = parse_color('BLUE')
    assert rgb == arcade.color.BLUE

    rgb = parse_color('DARK_BLUE')
    assert rgb == arcade.color.DARK_BLUE
