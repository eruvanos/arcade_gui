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
    def __init__(self, center_x, center_y, width=300,
                 height=40,
                 font_size=24,
                 outline_color=arcade.color.BLACK,
                 shadow_color=arcade.color.WHITE_SMOKE,
                 highlight_color=arcade.color.WHITE,
                 theme=None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.outline_color = outline_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.text = ""
        self.left_text = ""
        self.right_text = ""
        self.symbol = "|"
        self.cursor_index = 0
        self.theme = theme
        if self.theme:
            self.texture = self.theme.text_box_texture
            self.font_size = self.theme.font_size
            self.font_color = self.theme.font_color
            self.font_name = self.theme.font_name
        else:
            self.texture = None
            self.font_size = font_size
            self.font_color = arcade.color.BLACK
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

        arcade.draw_text(text_to_show,
                         self.center_x - self.width / 2.1,
                         self.center_y,
                         self.font_color,
                         font_size=self.font_size,
                         anchor_y="center",
                         font_name=self.font_name)

    #
    def color_theme_draw(self):

        if self.highlighted:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.highlight_color)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.shadow_color)

        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, self.outline_color, 2)
        self.draw_text()
        #

    # def texture_theme_draw(self):
    # arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
    # self.draw_text()

    def on_draw(self):
        # if self.texture:
        # self.texture_theme_draw()
        # else:
        self.color_theme_draw()


class UIInputBox(UIElement):
    def __init__(self,
                 x, y,
                 width=300, height=40,
                 theme=None,
                 outline_color=arcade.color.BLACK,
                 font_size=24,
                 shadow_color=arcade.color.WHITE_SMOKE,
                 highlight_color=arcade.color.WHITE, **kwargs):
        super().__init__(**kwargs)
        # self.theme = theme
        # if self.theme:
        #     self.text_display = TextDisplay(x, y, width, height, theme=self.theme)
        #     self.text_storage = TextStorage(width, theme=self.theme)
        # else:
        #     self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)

        self.text_adapter = KeyAdapter()
        self.text_display = TextDisplay(x, y, width, height, font_size, outline_color, shadow_color, highlight_color)

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
            self.text_adapter.on_event(event)

            # keep cursor_index in sync
            self.cursor_index = self.text_adapter.cursor_index
            self.text = self.text_adapter.text

    def on_focus(self):
        self.text_display.highlighted = True

    def on_unfocus(self):
        self.text_display.highlighted = False
