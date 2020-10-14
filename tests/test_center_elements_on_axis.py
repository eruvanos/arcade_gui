from arcade_gui.uilayout.anchor import UIAnchorLayout
from arcade_gui.uilayout.box import UIBoxLayout
from tests import dummy_element


# --- Strategy: AnchorLayout + fill_xy BorderLayout, align items
def test_anchor_layout_support_fill_option(parent):
    anchor = UIAnchorLayout(800, 600, parent=parent)
    box = UIBoxLayout(vertical=False)

    anchor.pack(box, bottom=0, left=0, fill_x=True)
    box.pack(dummy_element())
    anchor.refresh()

    assert box.width == 800
    assert box.height == 50


def test_box_align_items():
    box = UIBoxLayout(vertical=False, align='center')
    element = dummy_element()
    box.pack(element)
    box.width = 400

    box.refresh()

    assert element.center_x == 200
