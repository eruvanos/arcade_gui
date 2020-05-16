import arcade

from arcade_gui import UIElement


class UILabel(UIElement):
    def __init__(self, text, x, y,
                 font_color=None,
                 font_size=22,
                 anchor_x="center",
                 anchor_y="center",
                 width: int = 0,
                 align="center",
                 font_name=('Calibri', 'Arial'),
                 bold: bool = False,
                 italic: bool = False,
                 rotation=0, **kwargs):
        super().__init__(**kwargs)

        self.style_classes.append('uilabel')
        self.set_style_attrs(font_color=font_color)

        self.text = text
        self.x = x
        self.y = y
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
        font_color = self.find_color('font_color')

        arcade.draw_text(self.text,
                         self.x,
                         self.y,
                         font_color,
                         font_size=self.font_size,
                         anchor_x=self.anchor_x,
                         anchor_y=self.anchor_y,
                         width=self.width, align=self.align,
                         font_name=self.font_name, bold=self.bold,
                         italic=self.italic, rotation=self.rotation)
