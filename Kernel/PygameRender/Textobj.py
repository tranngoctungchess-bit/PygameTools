from typing import Union
import pygame
from Kernel.KernelWidget import MutableRect, ImmutableRect, Widget, MainScreen
from Kernel.ObjType import MathVal1, MathVal2, TextPack
from Kernel.VFlags import textpack
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
    def __init__(self, parent: Union[Widget, pygame.Surface, MainScreen], infomation_pack:  TextPack, rect: MathVal1, Uflags: tuple = ()):
        super().__init__(parent, rect)
        self.textpack = infomation_pack
        self.add_vflag(textpack, infomation_pack)
        self.Uflags = Uflags
        for uflag in Uflags:
            self.add_uflag(uflag)