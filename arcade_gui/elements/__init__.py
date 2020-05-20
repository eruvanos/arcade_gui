from arcade_gui import UIElement, UIEvent, MOUSE_PRESS, MOUSE_RELEASE


class UIAbstractButton(UIElement):
    """ Texture based UIElement supporting hover and press, this should fit every use case"""

    CLICKED = 'CLICKED'

    def __init__(self,
                 center_x=0, center_y=0,
                 width=None, height=None,
                 **kwargs):
        super().__init__(
            center_x=center_x, center_y=center_y, id=None
        )
        self.width = width
        self.height = height

        self.pressed = False
        self.hovered = False

        self.normal_texture = None
        self.mouse_over_texture = None
        self.mouse_press_texture = None

    def on_event(self, event: UIEvent):
        if event.type == MOUSE_PRESS and self.hover_point(event.x, event.y):
            self.on_press()
        elif event.type == MOUSE_RELEASE and self.pressed:
            if self.pressed:
                self.on_release()

                if self.hover_point(event.x, event.y):
                    self.on_click()
                    self.view.on_event(UIEvent(UIAbstractButton.CLICKED, ui_element=self))

    def set_proper_texture(self):
        """ Set normal, mouse-over, or clicked texture. """
        # TODO maybe call from UIView
        if self.pressed:
            self.texture = self.mouse_press_texture
        elif self.hovered:
            self.texture = self.mouse_over_texture
        else:
            self.texture = self.normal_texture

    def on_hover(self):
        self.hovered = True
        self.set_proper_texture()

    def on_unhover(self):
        self.hovered = False
        self.set_proper_texture()

    def on_press(self):
        self.pressed = True
        self.set_proper_texture()

    def on_release(self):
        self.pressed = False
        self.set_proper_texture()

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
