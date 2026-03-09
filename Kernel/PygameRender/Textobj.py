from typing import Union, Tuple
import pygame
from Kernel.Flags.UFlags import text_Is_Antialias
from Kernel.KernelWidget import Widget, MainScreen
from Kernel.ObjType import MathVal1, MathVal2, TextPack
from Kernel.Flags.VFlags import textpack
import re
def trashfunc(*args, **kwargs):
    pass
re_search = re.search
re_findall = re.findall
re_sub = re.sub
re_split = re.split
re_match = re.match
re_compile = re.compile
re_escape = re.escape
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
URL_PATTERN = re.compile(r'https?://\S+')
HASHTAG_PATTERN = re.compile(r'#\w+')
MENTION_PATTERN = re.compile(r'@\w+')
def extract_emails(text):
    return EMAIL_PATTERN.findall(text)
def extract_urls(text):
    return URL_PATTERN.findall(text)
def extract_hashtags(text):
    return HASHTAG_PATTERN.findall(text)
def safe_substitute(text, pattern, replacement):
    """Safe regex substitution với escape"""
    return re_sub(re_escape(pattern), replacement, text)
#wrap
SysFont = pygame.font.SysFont
Font = pygame.font.Font
class Label(Widget):
    __slots__ = ('font', 'textpack', 'smooth', 'bg')
    def __init__(self, parent: Union[Widget, pygame.Surface, MainScreen], color,
                 font, size, text,
                 name, Uflags: Union[set, tuple] = (), pos : MathVal2=(0,0)):
        self.textpack = TextPack(color, font, size, text)
        self.font = pygame.font.SysFont(self.textpack.Font, self.textpack.Size)
        text_surface = self.font.render(self.textpack.Text, False, self.textpack.Color)
        pygameRect = text_surface.get_rect()
        x,y = pos
        tuple_rect = (x,y,pygameRect.w, pygameRect.h)
        super().__init__(parent, rect=tuple_rect,name=name, can_change=True)
        self.add_vflag((textpack, TextPack(color, font, size, text)))
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