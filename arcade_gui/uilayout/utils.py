from abc import abstractmethod, ABC, abstractproperty

from arcade import Sprite


def right_of(sprite: Sprite) -> int:
    return int(sprite.center_x + sprite.width // 2)


def left_of(sprite: Sprite) -> int:
    return int(sprite.center_x - sprite.width // 2)


def top_of(sprite: Sprite) -> int:
    return int(sprite.center_y + sprite.height // 2)


def bottom_of(sprite: Sprite) -> int:
    return int(sprite.center_y - sprite.height // 2)


class DimensionMixin(ABC):
    """
    provides top,left,bottom,right,center_x,center_y,position for classes that rely on a list of elements.

    Requirements: iter(self)
    """

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @property
    def width(self) -> int:
        return int(self.right - self.left)

    @property
    def height(self) -> int:
        return int(self.top - self.bottom)

    @property
    def left(self) -> int:
        if len(self) == 0:
            return 0
        return int(min(map(left_of, self)))

    @left.setter
    def left(self, value):
        diff = value - self.left
        for element in self:
            element.left += diff

    @property
    def right(self) -> int:
        if len(self) == 0:
            return 0
        return int(max(map(right_of, self)))

    @right.setter
    def right(self, value):
        diff = value - self.right
        for element in self:
            element.right += diff

    @property
    def top(self) -> int:
        if len(self) == 0:
            return 0
        return int(max(map(top_of, self)))

    @top.setter
    def top(self, value):
        diff = value - self.top
        for element in self:
            element.top += diff

    @property
    def bottom(self) -> int:
        if len(self) == 0:
            return 0
        return int(min(map(bottom_of, self)))

    @bottom.setter
    def bottom(self, value):
        diff = value - self.bottom
        for element in self:
            element.bottom += diff

    @property
    def center_x(self) -> int:
        return int(self.left + self.width // 2)

    @center_x.setter
    def center_x(self, value):
        diff = value - self.center_x
        for element in self:
            element.center_x += diff

    @property
    def center_y(self) -> int:
        return int(self.bottom + self.height // 2)

    @center_y.setter
    def center_y(self, value):
        diff = value - self.center_y
        for element in self:
            element.center_y += diff

    @property
    def position(self):
        return self.center_x, self.center_y

    @position.setter
    def position(self, value):
        self.center_x, self.center_y = value


class OffsetDimensionMixin(ABC):
    """
    provides top,left,bottom,right,center_x,center_y,position for classes that rely on a list of elements.

    Requirements: iter(self)
    """

    # offset_x: int
    # offset_y: int

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @property
    def width(self) -> int:
        return int(self.right - self.left)

    @property
    def height(self) -> int:
        return int(self.top - self.bottom)

    @property
    def left(self) -> int:
        return self.offset_x

    @left.setter
    def left(self, value):
        diff = value - self.offset_x
        self.offset_x += diff

    @property
    def right(self) -> int:
        if len(self) == 0:
            return self.offset_x
        return int(max(map(right_of, self)))

    @right.setter
    def right(self, value):
        diff = value - self.right
        for element in self:
            element.right += diff

    @property
    def top(self) -> int:
        return self.offset_y

    @top.setter
    def top(self, value):
        diff = value - self.offset_y
        self.offset_y += diff

    @property
    def bottom(self) -> int:
        if len(self) == 0:
            return self.offset_y
        return int(min(map(bottom_of, self)))

    @bottom.setter
    def bottom(self, value):
        diff = value - self.offset_y
        self.offset_y += diff

    @property
    def center_x(self) -> int:
        return int(self.left + self.width // 2)

    @center_x.setter
    def center_x(self, value):
        diff = value - self.offset_x
        self.offset_x += diff

    @property
    def center_y(self) -> int:
        return int(self.top - self.height // 2)

    @center_y.setter
    def center_y(self, value):
        diff = value - self.offset_y
        self.offset_y += diff

    @property
    def position(self):
        return self.center_x, self.center_y

    @position.setter
    def position(self, value):
        self.center_x, self.center_y = value