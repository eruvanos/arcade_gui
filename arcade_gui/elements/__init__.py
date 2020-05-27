from typing import Optional

from arcade import Texture

from arcade_gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE, UIView


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

        self._normal_texture: Optional[Texture] = None
        self._hover_texture: Optional[Texture] = None
        self._press_texture: Optional[Texture] = None
        self._focus_texture: Optional[Texture] = None

    @property
    def normal_texture(self):
        return self._normal_texture

    @normal_texture.setter
    def normal_texture(self, texture: Texture):
        self._normal_texture = texture
        self.set_proper_texture()

    @property
    def hover_texture(self):
        return self._hover_texture

    @hover_texture.setter
    def hover_texture(self, texture: Texture):
        self._hover_texture = texture
        self.set_proper_texture()

    @property
    def press_texture(self):
        return self._press_texture

    @press_texture.setter
    def press_texture(self, texture: Texture):
        self._press_texture = texture
        self.set_proper_texture()

    @property
    def focus_texture(self):
        return self._focus_texture

    @focus_texture.setter
    def focus_texture(self, texture: Texture):
        self._focus_texture = texture
        self.set_proper_texture()

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
                    self.parent.on_event(UIEvent(UIClickable.CLICKED, ui_element=self))

    def set_proper_texture(self):
        """ Set normal, mouse-over, or clicked texture. """
        if self.pressed and self.press_texture:
            self.texture = self.press_texture
        elif self.focused and self.focus_texture:
            self.texture = self.focus_texture
        elif self.hovered and self.hover_texture:
            self.texture = self.hover_texture
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
        width = self.texture.width if self.texture else self.width
        height = self.texture.height if self.texture else self.height

        if hover_x > self.center_x + width / 2:
            return False
        if hover_x < self.center_x - width / 2:
            return False
        if hover_y > self.center_y + height / 2:
            return False
        if hover_y < self.center_y - height / 2:
            return False

        return True
