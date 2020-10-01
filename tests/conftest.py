import pytest
from arcade import Window

from arcade_gui.uilayout import UILayoutManager
from tests import MockParent


@pytest.fixture()
def window():
    window = Window()
    yield window
    window.close()


@pytest.fixture()
def ui_manager(window):
    mng = UILayoutManager(window)
    yield mng
    mng.unregister_handlers()


@pytest.fixture()
def parent():
    return MockParent(
        top=600,
        bottom=0,
        left=0,
        right=800
    )