import pytest

from arcade_gui import UIElement, UIView

DEFAULT_COLOR = (114, 47, 55)  # arcade.color.WINE
DEFAULT_COLOR_STR = str(DEFAULT_COLOR)[1:-1]
EXPECTED_COLOR = (135, 255, 104)
EXPECTED_COLOR_STR = str(EXPECTED_COLOR)[1:-1]


@pytest.fixture()
def element(view):
    view.style.style['uielement'] = {'font_color': DEFAULT_COLOR_STR}

    e = UIElement()
    e.style_classes.append('uielement')
    view.add_ui_element(e)

    yield e


def test_get_style_attribute_from_view(element):
    assert element.find_color('font_color') == DEFAULT_COLOR


def test_can_set_custom_style_attributes(element):
    element.set_style_attrs(font_color=EXPECTED_COLOR_STR)

    assert element.find_color('font_color') == EXPECTED_COLOR


def test_can_remove_custom_attributes(element):
    element.set_style_attrs(font_color=EXPECTED_COLOR_STR)

    element.set_style_attrs(font_color=None)

    assert element.find_color('font_color') == DEFAULT_COLOR


def test_ignores_del_of_attribute_if_they_are_set(element):
    element.set_style_attrs(font_color=None)

    assert element.find_color('font_color') == DEFAULT_COLOR


def test_attr_loaded_from_second_class(element):
    element.style_classes.append('some_class')
    assert element.find_color('font_color') == DEFAULT_COLOR


def test_loads_id_style_attributes_first(element):
    element_id = 'my_lovely_element'
    element.id = element_id

    view: UIView = element.view
    view.style.style[element_id] = {'font_color': EXPECTED_COLOR_STR}

    assert element.find_color('font_color') == EXPECTED_COLOR
