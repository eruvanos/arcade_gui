import pytest
from arcade import Window

from arcade_gui.layout import UIManager


@pytest.fixture()
def window():
    window = Window()
    yield window
    window.close()


@pytest.fixture()
def uimanager(window):
    mng = UIManager()
    yield mng
    mng.unregister_handlers()
