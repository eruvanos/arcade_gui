import pytest

from arcade_gui.uilayout.anchor import UIAnchorLayout
from arcade_gui.uilayout.box import UIBoxLayout
from tests import dummy_element


@pytest.fixture()
def layout(parent):
    return UIAnchorLayout(800, 600, parent=parent)


def test_anchor_bottom_left(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, bottom=100, left=10)
    layout.refresh()

    assert element_1.bottom == parent.bottom + 100
    assert element_1.left == parent.left + 10


def test_anchor_bottom_right(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, bottom=100, right=10)
    layout.refresh()

    assert element_1.bottom == parent.bottom + 100
    assert element_1.right == parent.right - 10


def test_anchor_top_right(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, top=100, right=10)
    layout.refresh()

    assert element_1.top == parent.top - 100
    assert element_1.right == parent.right - 10


def test_anchor_top_left(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, top=100, left=10)
    layout.refresh()

    assert element_1.top == parent.top - 100
    assert element_1.left == parent.left + 10


def test_anchor_layout_support_fill_x(parent):
    anchor = UIAnchorLayout(800, 600, parent=parent)
    box = UIBoxLayout(vertical=False)

    anchor.pack(box, bottom=0, left=0, fill_x=True)
    box.pack(dummy_element())
    anchor.refresh()

    assert box.width == 800
    assert box.height == 50


def test_anchor_layout_support_fill_y(parent):
    anchor = UIAnchorLayout(800, 600, parent=parent)
    box = UIBoxLayout(vertical=True)

    anchor.pack(box, bottom=0, left=0, fill_y=True)
    box.pack(dummy_element())
    anchor.refresh()

    assert box.width == 100
    assert box.height == 600


def test_anchor_center(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, center_x=0, center_y=0)
    layout.refresh()

    assert element_1.center_x == parent.center_x
    assert element_1.center_y == parent.center_y


def test_anchor_center_with_offset(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, center_x=10, center_y=-20)
    layout.refresh()

    assert element_1.center_x == parent.center_x + 10
    assert element_1.center_y == parent.center_y - 20
