import pytest

from arcade_gui.uilayout.box import UIBoxLayout
from tests import dummy_element


@pytest.fixture()
def v_layout(parent):
    return UIBoxLayout(parent=parent)


def test_vertical(v_layout, parent):
    v_layout.top = 200
    v_layout.left = 100

    element_1 = dummy_element()
    element_2 = dummy_element()

    v_layout.pack(element_1)
    v_layout.pack(element_2)
    v_layout.refresh()

    assert element_1.top == 200
    assert element_1.bottom == 150
    assert element_1.left == 100

    assert element_2.top == element_1.bottom
    assert element_2.left == 100


def test_vertical_with_spacing(v_layout, parent):
    v_layout.top = 200
    v_layout.left = 100

    element_1 = dummy_element()
    element_2 = dummy_element()

    v_layout.pack(element_1)
    v_layout.pack(element_2, space=10)
    v_layout.refresh()

    assert element_1.bottom == 150
    assert element_2.top == 140


@pytest.fixture()
def h_layout(parent):
    return UIBoxLayout(parent=parent, vertical=False)


def test_horizontal(h_layout, parent):
    h_layout.top = 200
    h_layout.left = 100

    element_1 = dummy_element()
    element_2 = dummy_element()

    h_layout.pack(element_1)
    h_layout.pack(element_2)
    h_layout.refresh()

    assert element_1.top == 200
    assert element_1.left == 100

    assert element_2.top == 200
    assert element_2.left == 200


def test_horizontal_with_spacing(h_layout, parent):
    h_layout.top = 200
    h_layout.left = 100

    element_1 = dummy_element()
    element_2 = dummy_element()

    h_layout.pack(element_1)
    h_layout.pack(element_2, space=10)
    h_layout.refresh()

    assert element_1.right == 200
    assert element_2.left == 210


def test_box_layout_updates_width_and_height(v_layout: UIBoxLayout):
    v_layout.pack(dummy_element(100, 50))

    assert v_layout.width == 100
    assert v_layout.height == 50

    v_layout.pack(dummy_element(150, 50), space=10)
    assert v_layout.width == 150
    assert v_layout.height == 110
