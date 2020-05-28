from typing import Optional
from uuid import uuid4

import arcade
from PIL import ImageDraw
from arcade.key import (
    MOTION_UP,
    MOTION_RIGHT,
    MOTION_DOWN,
    MOTION_LEFT,
    MOTION_END_OF_LINE,
    MOTION_NEXT_PAGE,
    MOTION_PREVIOUS_PAGE,
    MOTION_BEGINNING_OF_FILE,
    MOTION_END_OF_FILE,
    MOTION_BACKSPACE,
    MOTION_DELETE, MOTION_BEGINNING_OF_LINE,
)

from arcade_gui import UIEvent, TEXT_INPUT, TEXT_MOTION, UIClickable
from arcade_gui.utils import get_text_image


class KeyAdapter:
    """
    Handles the text and key inputs, primary storage of text and cursor_index.
    """

    def __init__(self, text=''):
        self._text = text
        self._cursor_index = 1
        self.state_changed = True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text != self._text:
            self.state_changed = True

        self._text = text

    @property
    def cursor_index(self):
        return self._cursor_index

    @cursor_index.setter
    def cursor_index(self, index):
        if index != self._cursor_index:
            self.state_changed = True

        self._cursor_index = index

    def reset_state_changed(self):
        self.state_changed = False

    def on_event(self, event):
        if event.type == TEXT_INPUT:
            text = event.text
            if text == '\r':
                return

            self.text = self.text[:self.cursor_index] + text + self.text[self.cursor_index:]
            self.cursor_index += len(text)

        elif event.type == TEXT_MOTION:
            motion = event.motion

            if motion == MOTION_UP:
                self.cursor_index = 0
            elif motion == MOTION_RIGHT:
                self.cursor_index += 1
            elif motion == MOTION_DOWN:
                self.cursor_index = len(self.text)
            elif motion == MOTION_LEFT:
                self.cursor_index -= 1
            # elif motion == MOTION_NEXT_WORD:
            #     pass
            # elif motion == MOTION_PREVIOUS_WORD:
            #     pass
            elif motion == MOTION_BEGINNING_OF_LINE:
                self.cursor_index = 0
            elif motion == MOTION_END_OF_LINE:
                self.cursor_index = len(self.text)
            elif motion == MOTION_NEXT_PAGE:
                self.cursor_index = len(self.text)
            elif motion == MOTION_PREVIOUS_PAGE:
                self.cursor_index = 0
            elif motion == MOTION_BEGINNING_OF_FILE:
                self.cursor_index = 0
            elif motion == MOTION_END_OF_FILE:
                self.cursor_index = len(self.text)
            elif motion == MOTION_BACKSPACE:
                self.text = self.text[:self.cursor_index - 1] + self.text[self.cursor_index:]
                self.cursor_index -= 1
            elif motion == MOTION_DELETE:
                self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]


class UIInputBox(UIClickable):
    ENTER = 'ENTER'

    def __init__(self,
                 parent,
                 center_x, center_y,
                 width,  # any way to not give width?
                 height=40,
                 text='',
                 id: Optional[str] = None,
                 **kwargs):
        super().__init__(
            parent,
            center_x=center_x,
            center_y=center_y,
            id=id,
            **kwargs
        )

        self.width = width
        self.height = height

        self.symbol = '|'
        self.text_adapter = KeyAdapter(text)

        self.normal_texture = None
        self.hover_texture = None
        self.focus_texture = None

        self.render_textures()

    def render_textures(self):
        """
        text got updated, so recreate textures
        """
        # TODO load defaults from style

        if self.text_adapter.state_changed:
            self.text_adapter.reset_state_changed()
        else:
            return

        font_name = ('Calibri', 'Arial')
        font_size = 22

        margin_left = 10
        align = "left"

        width = int(self.width)
        height = int(self.height)

        font_color = arcade.color.WHITE
        font_color_hover = arcade.color.WHITE
        font_color_active = arcade.color.BLACK

        DARK_GRAY = (21, 19, 21)
        bg_color = DARK_GRAY
        bg_color_hover = arcade.color.GRAY
        bg_color_active = arcade.color.GRAY

        border_width = 2
        border_color = arcade.color.WHITE
        border_color_hover = arcade.color.WHITE
        border_color_active = arcade.color.WHITE

        # text
        text_image_normal = get_text_image(text=self.text,
                                           font_color=font_color,
                                           font_size=font_size,
                                           font_name=font_name,
                                           align=align,
                                           width=width,
                                           height=height,
                                           valign='middle',
                                           indent=margin_left,
                                           background_color=bg_color
                                           )
        text_image_hover = get_text_image(text=self.text,
                                          font_color=font_color_hover,
                                          font_size=font_size,
                                          font_name=font_name,
                                          align=align,
                                          width=width,
                                          height=height,
                                          valign='middle',
                                          indent=margin_left,
                                          background_color=bg_color_hover
                                          )

        text_to_show = self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:]
        text_image_focus = get_text_image(text=text_to_show,
                                          font_color=font_color_active,
                                          font_size=font_size,
                                          font_name=font_name,
                                          align=align,
                                          width=width,
                                          height=height,
                                          valign='middle',
                                          indent=margin_left,
                                          background_color=bg_color_active
                                          )

        # draw outline
        rect = [0, 0, text_image_normal.width - border_width / 2, text_image_normal.height - border_width / 2]

        if border_color and border_width:
            d = ImageDraw.Draw(text_image_normal)
            d.rectangle(rect, fill=None, outline=border_color, width=border_width)

        if border_color_hover:
            d = ImageDraw.Draw(text_image_hover)
            d.rectangle(rect, fill=None, outline=border_color_hover, width=border_width)

        if border_color_active:
            d = ImageDraw.Draw(text_image_focus)
            d.rectangle(rect, fill=None, outline=border_color_active, width=border_width)

        self.normal_texture = arcade.Texture(image=text_image_normal, name=str(uuid4()))
        self.hover_texture = arcade.Texture(image=text_image_hover, name=str(uuid4()))
        self.focus_texture = arcade.Texture(image=text_image_focus, name=str(uuid4()))

    @property
    def cursor_index(self):
        return self.text_adapter.cursor_index

    @cursor_index.setter
    def cursor_index(self, value):
        value = min(len(self.text), value)
        value = max(0, value)

        self.text_adapter.cursor_index = value

    @property
    def text(self):
        return self.text_adapter.text

    @text.setter
    def text(self, value):
        self.text_adapter.text = value
        self.render_textures()

    def hover_point(self, hover_x: float, hover_y: float) -> bool:
        if hover_x > self.center_x + self.width / 2:
            return False
        if hover_x < self.center_x - self.width / 2:
            return False
        if hover_y > self.center_y + self.height / 2:
            return False
        if hover_y < self.center_y - self.height / 2:
            return False

        return True

    def on_event(self, event: UIEvent):
        super().on_event(event)

        if self.focused:
            if event.type == TEXT_INPUT and event.text == '\r':
                self.parent.on_event(UIEvent(UIInputBox.ENTER, ui_element=self))
                return

            self.text_adapter.on_event(event)

        self.render_textures()
