from arcade_gui.uilayout import UILayout


class UIAnchorLayout(UILayout):
    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)

        self._width = width
        self._height = height

    def place_elements(self):
        for element, data in self._elements:
            top = data.get('top')
            left = data.get('left')
            bottom = data.get('bottom')
            right = data.get('right')

            if bottom is not None:
                element.bottom = self.parent.bottom + bottom
            elif top is not None:
                element.top = self.parent.top - top

            if left is not None:
                element.left = self.parent.left + left
            elif right is not None:
                element.right = self.parent.right - right
