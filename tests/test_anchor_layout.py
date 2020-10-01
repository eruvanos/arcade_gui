import pytest

from arcade_gui.uilayout.anchor import UIAnchorLayout
from tests import dummy_element


@pytest.fixture()
def layout(parent):
    return UIAnchorLayout(parent=parent)


def test_anchor_bottom_left(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, bottom=100, left=10)

    assert element_1.bottom == parent.bottom + 100
    assert element_1.left == parent.left + 10


def test_anchor_bottom_right(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, bottom=100, right=10)

    assert element_1.bottom == parent.bottom + 100
    assert element_1.right == parent.right - 10


def test_anchor_top_right(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, top=100, right=10)

    assert element_1.top == parent.top - 100
    assert element_1.right == parent.right - 10


def test_anchor_top_left(layout, parent):
    element_1 = dummy_element()

    layout.pack(element_1, top=100, left=10)

    assert element_1.top == parent.top - 100
    assert element_1.left == parent.left + 10
