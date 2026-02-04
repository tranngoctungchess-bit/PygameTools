from typing import Union, Tuple
import pygame
from Kernel.UFlags import text_Is_Antialias
from Kernel.KernelWidget import MutableRect, ImmutableRect, Widget, MainScreen
from Kernel.ObjType import MathVal1, MathVal2, TextPack
from Kernel.VFlags import textpack
class Label(Widget):
    def __init__(self, parent: Union[Widget, pygame.Surface, MainScreen], infomation_pack:  TextPack,pos : MathVal2, Uflags: Union[set, tuple] = ()):
        self.font = pygame.font.SysFont(infomation_pack.Font, infomation_pack.Size)
        text_surface = self.font.render(infomation_pack.Text, False, infomation_pack.Color)
        pygameRect = text_surface.get_rect()
        x, y = pos
        tuple_rect = (x,y,pygameRect.w, pygameRect.h)
        super().__init__(parent, tuple_rect, can_change=True)
        self.textpack = infomation_pack
        self.add_vflag(textpack, infomation_pack)
        if isinstance(Uflags, set):
            self.uflags = Uflags
            self.dirty_uflags = Uflags
        else:
            for flag in Uflags:
                self.add_uflag(flag)
        self.smooth = text_Is_Antialias in self.uflags
        self.bg = None
    def smooth_update(self):
        self.smooth = text_Is_Antialias in self.uflags
    def Rect_update(self, rect: MathVal1):
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.rect.w = rect[2]
        self.rect.h = rect[3]
    def Size_update(self, size: MathVal2):
        self.rect.w = size[0]
        self.rect.h = size[1]