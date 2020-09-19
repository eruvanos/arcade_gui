import arcade
import pytest


@pytest.fixture()
def uimanager():

    mng = arcade.gui

    yield