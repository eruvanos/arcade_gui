import arcade
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

from arcade_gui import UIElement, UIEvent, TEXT_INPUT, TEXT_MOTION


class KeyAdapter:
    def __init__(self):
        self.text = ""
        self.cursor_index = 1

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


class TextDisplay:
    def __init__(self,
                 parent: UIElement,
                 center_x,
                 center_y,
                 width=300,
                 height=40,
                 font_size=24
                 ):
        self.parent = parent

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

        self.text = ""
        self.symbol = "|"
        self.cursor_index = 0
        self.highlighted = False

        # Style
        self.font_size = font_size
        self.font_name = ('Calibri', 'Arial')

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

    def draw_text(self):
        if self.text == '' and not self.highlighted:
            return

        if self.highlighted:
            text_to_show = self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:]
        else:
            text_to_show = self.text

        font_color = self.parent.find_color('font_color')
        arcade.draw_text(text_to_show,
                         self.center_x - self.width / 2.1,
                         self.center_y,
                         font_color,
                         font_size=self.font_size,
                         anchor_y="center",
                         font_name=self.font_name)

    def on_draw(self):
        normal_color = self.parent.find_color('normal_color')
        shadow_color = self.parent.find_color('shadow_color')
        highlight_color = self.parent.find_color('highlight_color')

        if self.highlighted:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, highlight_color)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, shadow_color)

        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, normal_color, 2)
        self.draw_text()


class UIInputBox(UIElement):
    ENTER = 'ENTER'

    def __init__(self,
                 center_x, center_y,
                 width=300, height=40,
                 font_size=24,
                 normal_color=None,
                 shadow_color=None,
                 highlight_color=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.text_adapter = KeyAdapter()
        self.text_display = TextDisplay(self, center_x, center_y, width, height, font_size)

        self.style_classes.append('inputbox')
        self.set_style_attrs(
            normal_color=normal_color,
            shadow_color=shadow_color,
            highlight_color=highlight_color
        )

    @property
    def cursor_index(self):
        return self.text_display.cursor_index

    @cursor_index.setter
    def cursor_index(self, value):
        value = min(len(self.text), value)
        value = max(0, value)

        self.text_display.cursor_index = value
        self.text_adapter.cursor_index = value

    @property
    def text(self):
        return self.text_adapter.text

    @text.setter
    def text(self, value):
        self.text_adapter.text = value
        self.text_display.text = value

    def on_draw(self):
        self.text_display.on_draw()

    def hover_point(self, hover_x: float, hover_y: float) -> bool:
        return self.text_display.hover_point(hover_x, hover_y)

    def on_event(self, event: UIEvent):
        super().on_event(event)

        if self.text_display.highlighted:
            if event.type == TEXT_INPUT and event.text == '\r':
                self.view.on_event(UIEvent(UIInputBox.ENTER, ui_element=self))
                return

            self.text_adapter.on_event(event)

            # keep cursor_index in sync
            self.cursor_index = self.text_adapter.cursor_index
            self.text = self.text_adapter.text

    def on_focus(self):
        self.text_display.highlighted = True

    def on_unfocus(self):
        self.text_display.highlighted = False
