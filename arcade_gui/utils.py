import os
import sys
from pathlib import Path
from typing import Union


def create_resource_path(relative_path: Union[str, Path]):
    """
    Get absolute path to resource, works for dev and for PyInstaller's 'onefile' mode

    :param relative_path: A relative path to a file of some kind.

    """

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # pylint: disable=no-member,protected-access
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
