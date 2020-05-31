from uuid import uuid4

import pytest

from arcade_gui import UIView, UIElement, UIException
from tests import MockButton


def test_ui_elements_get_reference_to_view():
    view = UIView()
    ui_element = MockButton()

    view.add_ui_element(ui_element)

    assert ui_element.view == view


def test_can_search_ui_elements_by_id(view):
    mock_button = MockButton(id=str(uuid4()))

    view.add_ui_element(mock_button)

    assert view.find_by_id(mock_button.id) == mock_button


def test_can_set_id_after_creation(view, mock_button):
    mock_button.id = str(uuid4())

    view.add_ui_element(mock_button)

    assert view.find_by_id(mock_button.id) == mock_button


def test_find_by_id_returns_none():
    view = UIView()
    assert view.find_by_id('no element here') is None


def test_duplicate_ids_raise_an_ui_exception(view):
    ui_element_1 = MockButton(id='element1')
    ui_element_2 = MockButton(id='element1')
    view.add_ui_element(ui_element_1)

    with pytest.raises(UIException) as e:
        view.add_ui_element(ui_element_2)

    assert 'duplicate id "element1"' in str(e.value)


def test_broken_ui_element_raises():
    view = UIView()

    # noinspection PyMissingConstructor
    class BrokenUIElement(UIElement):
        def __init__(self):
            pass

    with pytest.raises(UIException) as e:
        view.add_ui_element(BrokenUIElement())

    assert 'super().__init__' in str(e.value)


def test_no_id_duplication_exception_after_purge(view):
    # GIVEN
    view.add_ui_element(MockButton(id='dream'))

    # WHEN
    view.purge_ui_elements()

    # THEN
    view.add_ui_element(MockButton(id='dream'))
