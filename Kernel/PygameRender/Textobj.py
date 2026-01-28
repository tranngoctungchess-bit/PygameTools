from typing import Union
import pygame
from Kernel.KernelWidget import MutableRect, ImmutableRect, Widget
from Kernel.ObjType import MathVal1, MathVal2, TextPack
"""
Text has 6 uflags:
- IsItalic
- IsBold
- IsUnderline
- IsUnderscore
- CanClick (the widget uflag)
- CanHover (the widget uflag)
- ...(the widget uflag)
And 4 vflags:
- Color
- Size
- Thickness
- Font
and 4 uflags must be exsist! so I can get a normal class
"""
class Label(Widget):
    def __init__(self, infomation_pack:  TextPack, Uflags: tuple, rect: MathVal1):
        super().__init__(rect)
        self.textpack = infomation_pack
        self.Uflags = Uflags