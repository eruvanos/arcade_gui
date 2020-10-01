from unittest.mock import Mock

import pytest

from tests import dummy_element


def test_add_element_directly_to_manager_warns(ui_manager):
    with pytest.warns(UserWarning):
        ui_manager.add_ui_element(dummy_element())


def test_layout_change_triggers_refresh(ui_manager):
    ui_manager.lazy_refresh = False
    ui_manager.root_layout.refresh = Mock()

    ui_manager.root_layout.changed()

    assert ui_manager.root_layout.refresh.called


def test_layout_change_triggers_not_if_lazy_refresh_is_set(ui_manager):
    ui_manager.lazy_refresh = True
    ui_manager.root_layout.refresh = Mock()

    ui_manager.root_layout.changed()

    assert not ui_manager.root_layout.refresh.called


def test_refresh_refreshes_element_list(ui_manager):
    ui_manager.lazy_refresh = True

    ui_manager.root_layout.pack(dummy_element())
    assert len(ui_manager._ui_elements) == 0

    ui_manager.refresh()
    assert len(ui_manager._ui_elements) == 1


def test_added_element_to_child_layout_is_added_to_layout_manager(ui_manager):
    ui_manager.lazy_refresh = False

    ui_manager.root_layout.pack(dummy_element())
    assert len(ui_manager._ui_elements) == 1
