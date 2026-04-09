from collections import namedtuple
RectTuple = tuple[int | float,int | float,int | float,int | float]
PosTuple = tuple[int | float,int | float]
class Border:
    def __init__(self, border_width, border_color):
        self.border_width = border_width
        self.border_col = border_color
class TextPack:
    __slots__ = ('Color', 'Font', 'Size', 'Text')
    def __init__(self, Color, Font, Size, Text):
        self.Color = Color
        self.Font = Font
        self.Size = Size
        self.Text = Text