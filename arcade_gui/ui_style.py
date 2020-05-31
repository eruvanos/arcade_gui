from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Any

import yaml
from PIL.ImageColor import getrgb

import arcade_gui
from arcade_gui.utils import parse_value

if TYPE_CHECKING:
    pass


class UIStyle:
    """
    Used as singleton in the UIView, style changes are applied by changing the values of the singleton.

    Use `.load()` to update UIStyle instance from YAML-file


    """

    def __init__(self, data: Dict, **kwargs):
        super().__init__(**kwargs)
        self.style = data

    @staticmethod
    def load(path: Path):
        """
        Load style from a file, overwriting existing data

        :param path:
        """
        with path.open() as file:
            data: Dict[str, Dict[str, Any]] = yaml.safe_load(file)
            assert isinstance(data, dict)

        # parse values, expected structure Dict[class, Dict[key, value]]
        for style_class, style_data in data.items():
            for key, value in style_data.items():
                style_data[key] = parse_value(value)

        return UIStyle(data)

    @staticmethod
    @lru_cache
    def default_style():
        """
        :return: empty style # TODO maybe load the real default style once
        """
        return UIStyle.load(arcade_gui.resources.path('style/default.yml'))

    def get_class(self, key: str):
        return self.style.setdefault(key, {})

    def get_attr(self, style_classes: List[str], attr: str):
        """
        Retrieves an attribute, resolved from style by style_classes

        :param style_classes: List of style classes, resolving from right to left
        :param attr: attribute name to get value for
        :return: value of the attribute, first found
        """
        style_classes = reversed(style_classes)
        for style_class in style_classes:
            style_data = self.style.get(style_class, {})
            attr_value = style_data.get(attr)
            if attr_value:
                return attr_value
        else:
            return None
