from arcade_gui.elements import UISpace


def test_spacer_has_defined_size():
    spacer = UISpace(100, 200)
    assert spacer.width == 100
    assert spacer.height == 200
