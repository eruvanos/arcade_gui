"""
Tests if examples render and show the same screen like expected
"""
import os
import sys
from importlib import import_module
from pathlib import Path

import arcade
import pyglet
import pytest

from tests import T


@pytest.fixture(scope='session')
def window():
    yield arcade.Window(title='ARCADE_GUI')


def view_to_png(window: arcade.Window, view: arcade.View, path: Path):
    window.clear()

    window.show_view(view)
    view.on_update(0)
    view.on_draw()

    arcade.finish_render()
    arcade.finish_render()  # Not sure, why this is required, but just see a black screen otherwise

    pyglet.image.get_buffer_manager().get_color_buffer().save(str(path))


def files_equal(file1: Path, file2: Path):
    return file1.read_bytes() == file2.read_bytes()


def load_view(abs_module_path) -> arcade.View:
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, 'MyView')

    assert isinstance(target_class, arcade.View)
    return target_class


@pytest.mark.skipif(os.getenv('TRAVIS') == 'true',
                    reason=('Example tests not executable on travis, '
                            'check https://travis-ci.org/github/eruvanos/arcade_gui/jobs/678758144#L506'))
@pytest.mark.skipif(sys.platform == 'darwin', reason='Not yet supported on darwin')
@pytest.mark.parametrize('example', [
    T('show_id_example', 'show_id_example'),
    T('show_uibutton', 'show_uibutton'),
    T('show_uiinputbox', 'show_uiinputbox'),
    T('show_uilabel', 'show_uilabel')
])
def test_id_example(window, tmp_path, example):
    expected_screen = Path(f'assets/{example}.png')

    # import example view
    MyView = import_module(f'examples.{example}').MyView

    # Render View and take screen shot
    actual_screen = tmp_path / f'{example}.png'
    view_to_png(window, MyView(), actual_screen)

    # compare files
    assert expected_screen.exists(), f'expected screen missing, actual at {actual_screen}'
    assert files_equal(expected_screen, actual_screen)
