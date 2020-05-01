from typing import Dict, Optional

import arcade


class SubmitButton(TextButton):
    def __init__(self, textbox, on_submit, x, y, width=100, height=40, text="submit", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.textbox = textbox
        self.on_submit = on_submit

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.on_submit()
            self.textbox.text_adapter.text = ""
            self.textbox.text_display.text = ""


class DialogueBox:
    def __init__(self, x, y, width, height, color=None, theme=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.active = False
        self.button_list = []
        self.text_list = []
        self.theme = theme
        if self.theme:
            self.texture = self.theme.dialogue_box_texture

    def on_draw(self):
        if self.active:
            if self.theme:
                arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
            else:
                arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
            for button in self.button_list:
                button.on_draw()
            for text in self.text_list:
                text.on_draw()

    def on_mouse_press(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, _button, _modifiers):
        for button in self.button_list:
            button.check_mouse_release(x, y)




class TextDisplay:
    def __init__(self, x, y, width=300, height=40, outline_color=arcade.color.BLACK,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE, theme=None):
        self.x = x
        self.y = y
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
            self.font_size = 24
            self.font_color = arcade.color.BLACK
            self.font_name = ('Calibri', 'Arial')

    def draw_text(self):
        if self.highlighted:
            arcade.draw_text(self.text[:self.cursor_index] + self.symbol + self.text[self.cursor_index:],
                             self.x - self.width / 2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)
        else:
            arcade.draw_text(self.text, self.x - self.width / 2.1, self.y, self.font_color, font_size=self.font_size,
                             anchor_y="center", font_name=self.font_name)

    def color_theme_draw(self):
        if self.highlighted:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.highlight_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.shadow_color)
        self.draw_text()
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, self.outline_color, 2)

    def texture_theme_draw(self):
        arcade.draw_texture_rectangle(self.x, self.y, self.width, self.height, self.texture)
        self.draw_text()

    def draw(self):
        if self.texture == "":
            self.color_theme_draw()
        else:
            self.texture_theme_draw()

    def on_press(self):
        self.highlighted = True

    def on_release(self):
        pass

    def on_mouse_press(self, x, y, _button, _modifiers):
        if x > self.x + self.width / 2:
            self.highlighted = False
            return
        if x < self.x - self.width / 2:
            self.highlighted = False
            return
        if y > self.y + self.height / 2:
            self.highlighted = False
            return
        if y < self.y - self.height / 2:
            self.highlighted = False
            return
        self.on_press()

    def on_mouse_release(self, x, y, _button, _modifiers):
        if self.highlighted:
            self.on_release()

    def update(self, _delta_time, text, symbol, cursor_index):
        self.text = text
        self.symbol = symbol
        self.cursor_index = cursor_index




class TextBox:
    def __init__(self, x, y, width=300, height=40, theme=None, outline_color=arcade.color.BLACK, font_size=24,
                 shadow_color=arcade.color.WHITE_SMOKE, highlight_color=arcade.color.WHITE):
        self.theme = theme
        if self.theme:
            self.text_display = TextDisplay(x, y, width, height, theme=self.theme)
            self.text_storage = TextStorage(width, theme=self.theme)
        else:
            self.text_display = TextDisplay(x, y, width, height, outline_color, shadow_color, highlight_color)
            self.text_storage = TextStorage(width, font_size)
        self.text = ""

    def draw(self):
        self.text_display.draw()

    def update(self, delta_time, key):
        if self.text_display.highlighted:
            self.text, symbol, cursor_index = self.text_storage.update(delta_time, key)
            self.text_display.update(delta_time, self.text, symbol, cursor_index)

    def check_mouse_press(self, x, y):
        self.text_display.check_mouse_press(x, y)

    def check_mouse_release(self, x, y):
        self.text_display.check_mouse_release(x, y)


class Theme:
    DEFAULT_FONT_COLOR = arcade.color.BLACK
    DEFAULT_FONT_SIZE = 24
    DEFAULT_FONT_NAME = ('Calibri', 'Arial')

    def __init__(self):
        self.button_textures: Dict[str, Optional['', arcade.Texture]] = \
            {'normal': '', 'hover': '', 'clicked': '', 'locked': '', }
        self.menu_texture = ""
        self.window_texture = ""
        self.dialogue_box_texture = ""
        self.text_box_texture = ""
        self.font_color = self.__class__.DEFAULT_FONT_COLOR
        self.font_size = self.__class__.DEFAULT_FONT_SIZE
        self.font_name = self.__class__.DEFAULT_FONT_NAME

    def add_button_textures(self, normal, hover=None, clicked=None, locked=None):
        normal_texture = arcade.load_texture(normal)
        self.button_textures['normal'] = normal_texture

        self.button_textures['hover'] = arcade.load_texture(hover) \
            if hover is not None else normal_texture
        self.button_textures['clicked'] = arcade.load_texture(clicked) \
            if clicked is not None else normal_texture
        self.button_textures['locked'] = arcade.load_texture(locked) \
            if locked is not None else normal_texture

    def add_window_texture(self, window_texture):
        self.window_texture = arcade.load_texture(window_texture)

    def add_menu_texture(self, menu_texture):
        self.menu_texture = arcade.load_texture(menu_texture)

    def add_dialogue_box_texture(self, dialogue_box_texture):
        self.dialogue_box_texture = arcade.load_texture(dialogue_box_texture)

    def add_text_box_texture(self, text_box_texture):
        self.text_box_texture = arcade.load_texture(text_box_texture)

    def set_font(self, font_size, font_color, font_name=None):
        self.font_color = font_color
        self.font_size = font_size
        self.font_name = font_name \
            if font_name is not None \
            else self.__class__.DEFAULT_FONT_NAME
