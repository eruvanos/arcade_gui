from typing import Optional, Union

import PIL
import arcade
from arcade.gui import UIElement, UIException

from arcade_gui.uilayout import UILayout


class UISpace(UILayout):
    """
    Empty space, fix size
    """

    def __init__(
            self,
            width,
            height,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.height = height
        self.width = width

    def refresh(self):
        pass

    def pack(self, element: Union['UILayout', UIElement], **kwargs):
        raise NotImplementedError(f'Not supported on a {UISpace.__name__}')

    def place_elements(self):
        pass


class UIBox(UIElement):
    """
    Simple UIElement, showing either a given texture or a solid color.
    """

    def __init__(self,
                 center_x=0,
                 center_y=0,
                 width: int = None,
                 height: int = None,
                 color: Optional[arcade.Color] = None,
                 texture: Optional[arcade.Texture] = None,
                 **kwargs):
        super().__init__(
            center_x=center_x,
            center_y=center_y,
            **kwargs
        )

        if None not in (width, height, color):
            image = PIL.Image.new('RGBA', (width, height), color)
            self.texture = arcade.Texture(f"Solid-{color[0]}-{color[1]}-{color[2]}", image, hit_box_algorithm='None')
        elif texture:
            self.texture = texture
        else:
            raise UIException('UIBox requires either (color, width, height) or texture to be set')

    def render(self):
        pass
