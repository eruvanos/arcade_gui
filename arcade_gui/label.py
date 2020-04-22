import arcade

from arcade_gui import UIElement


class UILabel(UIElement):
    def __init__(self, text, x, y,
                 color=arcade.color.BLACK,
                 font_size=22,
                 anchor_x="center",
                 anchor_y="center",
                 width: int = 0,
                 align="center",
                 font_name=('Calibri', 'Arial'),
                 bold: bool = False,
                 italic: bool = False,
                 rotation=0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.width = width
        self.align = align
        self.font_name = font_name
        self.bold = bold
        self.italic = italic
        self.rotation = rotation
        self.active = True

    def on_draw(self):
        arcade.draw_text(self.text,
                         self.x,
                         self.y,
                         self.color,
                         font_size=self.font_size,
                         anchor_x=self.anchor_x,
                         anchor_y=self.anchor_y,
                         width=self.width, align=self.align,
                         font_name=self.font_name, bold=self.bold,
                         italic=self.italic, rotation=self.rotation)
