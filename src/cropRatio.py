
class CropRatio:

    def __init__(self, left, top, right, bottom):
        self._left = left
        self._top = top
        self._right = right
        self._bottom = bottom

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def right(self):
        return self._right

    @property
    def bottom(self):
        return self._bottom