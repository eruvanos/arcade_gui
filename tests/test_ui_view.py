from arcade_gui import UIView, UIElement


def test_ui_elements_get_reference_to_view():
    view = UIView()
    ui_element = UIElement()

    view.add_ui_element(ui_element)

    assert ui_element.view == view
