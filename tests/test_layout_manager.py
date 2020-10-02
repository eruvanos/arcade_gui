from unittest.mock import Mock

import pytest

from tests import dummy_element


def test_add_element_directly_to_manager_warns(ui_manager):
    with pytest.warns(UserWarning):
        ui_manager.add_ui_element(dummy_element())


def test_update_does_not_trigger_refresh(ui_manager):
    ui_manager.root_layout.refresh = Mock()

    ui_manager.on_update(0)

    assert not ui_manager.root_layout.refresh.called


def test_update_triggers_refresh_if_changed(ui_manager):
    ui_manager.root_layout.refresh = Mock()
    ui_manager.root_layout.changed()

    ui_manager.on_update(0)

    assert ui_manager.root_layout.refresh.called
