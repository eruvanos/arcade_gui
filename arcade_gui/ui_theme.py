from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from arcade_gui import UIElement


class UITheme:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def load(path: Path) -> 'UITheme':
        with path.open() as file:
            data = yaml.safe_load(file)
        return UITheme(data)

    # TODO maybe move this logic into ui_element, makes overwriting themes easier later
    @staticmethod
    def resolve(ui_element: 'UIElement', param: str):
        view = ui_element.view
        theme = view.theme
        return theme.get(ui_element, param)

    def get(self, ui_element, param):
        lookup_name = type(ui_element).__name__.lower()
        flatbutton_data = self.data.get(lookup_name, {})
        return flatbutton_data.get(param)
