import arcade_gui


class TestUIView(arcade_gui.UIView):

    def click_and_hold(self, x: int, y: int):
        self.on_event(arcade_gui.UIEvent(
            arcade_gui.MOUSE_PRESS,
            x=x,
            y=y,
            button=1,
            modifier=0
        ))

    def release(self, x: int, y: int):
        self.on_event(arcade_gui.UIEvent(
            arcade_gui.MOUSE_RELEASE,
            x=x,
            y=y,
            button=1,
            modifier=0
        ))

    def click(self, x: int, y: int):
        self.click_and_hold(x, y)
        self.release(x, y)
