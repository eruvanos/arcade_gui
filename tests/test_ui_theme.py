from arcade_gui import FlatButton, GhostFlatButton, UI3DButton

from arcade_gui.ui_theme import UITheme


def test_view_loads_default_theme(view):
    assert view.theme is not None


def test_get_property_from_red_theme(shared_datadir, view):
    theme = UITheme.load(shared_datadir / 'red_theme.yml')
    view.theme = theme

    button = FlatButton('Love snakes.', 100, 100, 100, 30)
    view.add_ui_element(button)

    assert UITheme.resolve(button, 'normal_color') == 'RED'


def test_get_property_for_blue_theme(shared_datadir, view):
    theme = UITheme.load(shared_datadir / 'blue_theme.yml')
    view.theme = theme

    button = FlatButton('Love snakes.', 100, 100, 100, 30)
    view.add_ui_element(button)

    assert UITheme.resolve(button, 'normal_color') == 'BLUE'


def test_theme_returns_property_for_ui_elements(shared_datadir, view):
    theme = UITheme({
        'flatbutton': {'normal_color': 'RED'},
        'ghostflatbutton': {'normal_color': 'BLUE'},
    })
    flat = FlatButton('Love snakes.', 100, 100, 100, 30)
    ghost = GhostFlatButton('Love snakes.', 100, 100, 100, 30)

    assert theme.get(flat, 'normal_color') == 'RED'
    assert theme.get(ghost, 'normal_color') == 'BLUE'


def test_theme_returns_none_for_unknown_ui_element_class(shared_datadir, view):
    theme = UITheme({
        'flatbutton': {'normal_color': 'RED'},
    })
    button = UI3DButton('Love snakes.', 100, 100, 100, 30)

    assert theme.get(button, 'normal_color') is None
