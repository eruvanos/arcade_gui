import arcade
import pytest

from arcade_gui import UIElement, UIView

ELEMENT_STYLE_CLASS = 'uielement'

DEFAULT_COLOR = (114, 47, 55)  # arcade.color.WINE
DEFAULT_COLOR_STR = str(DEFAULT_COLOR)[1:-1]
EXPECTED_COLOR = (135, 255, 104)
EXPECTED_COLOR_STR = str(EXPECTED_COLOR)[1:-1]


@pytest.fixture()
def element(view):
    view.style.style[ELEMENT_STYLE_CLASS] = {'normal_color': DEFAULT_COLOR_STR}

    e = UIElement()
    e.style_classes.append(ELEMENT_STYLE_CLASS)
    view.add_ui_element(e)

    yield e


def test_get_style_attribute_from_view_by_element_class(element):
    assert element.find_color('normal_color') == DEFAULT_COLOR


def test_fallback_to_global_values(element):
    attr_not_set_in_class_style = 'font_color'

    assert element.find_color(attr_not_set_in_class_style) == arcade.color.BLACK


def test_can_set_custom_style_attributes(element):
    element.set_style_attrs(normal_color=EXPECTED_COLOR_STR)

    assert element.find_color('normal_color') == EXPECTED_COLOR


def test_can_remove_custom_attributes(element):
    element.set_style_attrs(normal_color=EXPECTED_COLOR_STR)

    element.set_style_attrs(normal_color=None)

    assert element.find_color('normal_color') == DEFAULT_COLOR


def test_ignores_del_of_attribute_if_they_are_set(element):
    element.set_style_attrs(normal_color=None)

    assert element.find_color('normal_color') == DEFAULT_COLOR


def test_attr_loaded_from_second_class(element):
    element.style_classes.append('some_class')
    assert element.find_color('normal_color') == DEFAULT_COLOR


def test_loads_id_style_attributes_first(element):
    element_id = 'my_lovely_element'
    element.id = element_id

    view: UIView = element.view
    view.style.style[element_id] = {'normal_color': EXPECTED_COLOR_STR}

    assert element.find_color('normal_color') == EXPECTED_COLOR
