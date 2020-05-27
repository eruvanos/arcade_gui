from typing import Optional

import PIL
import arcade
from PIL import ImageDraw
from PIL.Image import Image
from arcade import Color

from arcade_gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE, UIView
from arcade_gui.utils import get_text_image, get_image_with_text


class UIClickable(UIElement):
    """ Texture based UIElement supporting hover and press, this should fit every use case"""

    CLICKED = 'UIClickable_CLICKED'

    def __init__(self,
                 parent: UIView,
                 center_x=0, center_y=0,
                 *args,
                 **kwargs):
        super().__init__(
            parent,
            center_x=center_x,
            center_y=center_y,
        )

        self._pressed = False
        self._hovered = False
        self._focused = False

        self.normal_texture = None
        self.hover_texture = None
        self.press_texture = None
        self.focus_texture = None

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, value):
        self._hovered = value
        self.set_proper_texture()

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value
        self.set_proper_texture()

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        self._focused = value
        self.set_proper_texture()

    def on_event(self, event: UIEvent):
        if event.type == MOUSE_PRESS and self.hover_point(event.x, event.y):
            self.on_press()
        elif event.type == MOUSE_RELEASE and self.pressed:
            if self.pressed:
                self.on_release()

                if self.hover_point(event.x, event.y):
                    self.on_click()
                    self.view.on_event(UIEvent(UIClickable.CLICKED, ui_element=self))

    def set_proper_texture(self):
        """ Set normal, mouse-over, or clicked texture. """
        if self.pressed and self.press_texture:
            self.texture = self.press_texture
        elif self.hovered and self.hover_texture:
            self.texture = self.hover_texture
        elif self.focused and self.focus_texture:
            self.texture = self.focus_texture
        else:
            self.texture = self.normal_texture

    def on_hover(self):
        self.hovered = True

    def on_unhover(self):
        self.hovered = False

    def on_focus(self):
        self.focused = True

    def on_unfocus(self):
        self.focused = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def on_click(self):
        pass

    def hover_point(self, hover_x: float, hover_y: float) -> bool:
        width = self.width if self.width else 0
        height = self.height if self.height else 0

        if hover_x > self.center_x + width / 2:
            return False
        if hover_x < self.center_x - width / 2:
            return False
        if hover_y > self.center_y + height / 2:
            return False
        if hover_y < self.center_y - height / 2:
            return False

        return True


def render_text_image(
        text: str,

        font_size=22,
        font_name=('Calibri', 'Arial'),
        font_color: Color = arcade.color.WHITE,

        border_width: int = 2,
        border_color: Optional[Color] = arcade.color.WHITE,

        align: str = "left",
        valign: str = "top",

        bg_color: Optional[Color] = None,
        bg_image: Optional[Image] = None,

        width: Optional[int] = None,
        height: Optional[int] = None,
        indent: int = 0
):
    if bg_image:

        if width:
            if not height:
                height = bg_image.height
            bg_image.resize((width, height), resample=PIL.Image.LANCZOS)

        image = get_image_with_text(
            text,
            font_name=font_name,
            font_color=font_color,
            font_size=font_size,

            background_image=bg_image,
            align=align,
            valign=valign,
            indent=indent
        )
    else:
        image = get_text_image(
            text,
            font_name=font_name,
            font_color=font_color,
            font_size=font_size,

            background_color=bg_color,
            align=align,
            valign=valign,
            indent=indent,

            width=width if width else 0,
            height=height
        )

    # add margin
    # margin = (10, 15, 10, 15)
    # image = add_margin(image, *margin, bg_color)

    # draw outline
    rect = [0,
            0,
            image.width - border_width / 2,
            image.height - border_width / 2]

    if border_color and border_width:
        d = ImageDraw.Draw(image)
        d.rectangle(rect, fill=None, outline=border_color, width=border_width)

    return image
