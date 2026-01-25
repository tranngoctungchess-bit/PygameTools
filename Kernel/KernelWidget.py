import numpy as np
from typing import Tuple, Union, Optional, List, Dict, Any
from dataclasses import dataclass
from collections import namedtuple
import pygame
from Kernel.ObjType import MathVal2, MathVal1
from Kernel.UFlags import *
from Kernel.VFlags import *
class ValuePackTypeError(Exception):
    def __init__(self, message):
        super().__init__(message)
"""
ImmutableRect and MutableRect:
the base object for any widget class as bar, button coming soon in this tool
x, y: the pos of rect
width, height: the width and the height of this rect
"""
ImmutableRect = namedtuple('Rect', ['x', 'y', 'w', 'h'])
Position = namedtuple('Pos', ['x', 'y']) #create to look code easier
@dataclass(slots = True)
class MutableRect:
    x:Union[int, float]
    y:Union[int,float]
    w:Union[int, float]
    h:Union[int,float]
class Widget:
    """
    Docstring for Widget
    rect: the rect of this widget
    is_dirty: whether this widget is changed
    uflags: the unchangeable flags set for this widget
    vflags: the changeable flags dict for this widget
    dirty_uflags: the changed unchangeable flags set for this widget
    dirty_vflags: the changed changeable flags set for this widget
    pos_x: the x positions list for all objects in this widget
    pos_y: the y positions list for all objects in this widget
    """
    __slots__ = ('rect', 'is_dirty', 'uflags', 'vflags', 'dirty_uflags', 'dirty_vflags', 'pos_x', 'pos_y')
    def __init__(self, rect: MathVal1, can_change = False):
        self.rect = ImmutableRect(*rect) if not can_change else MutableRect(*rect)
        self.is_dirty = False
        self.uflags = set()
        self.vflags = {}
        self.dirty_uflags = set()
        self.dirty_vflags = set()
        self.pos_x = []
        self.pos_y = []
    def add_obj(self, pos: MathVal2):
        self.pos_x.append(pos[0])
        self.pos_y.append(pos[1])
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
    def get_pos(self):
        return self.rect.x, self.rect.y
    def get_size(self):
        return self.rect.w, self.rect.h
    def set_flags(self, uflags: tuple=(), vflags: tuple=()):
        for uflag in uflags:
            self.uflags.add(uflag)
            self.dirty_uflags.add(uflag)
        for pack in vflags:
            self.vflags[pack[0]] = pack[1]
            self.dirty_vflags.add(pack[0])
        self.is_dirty = True
    def add_uflag(self, uflag):
        self.uflags.add(uflag)
        self.dirty_uflags.add(uflag)
        self.is_dirty = True
    def add_vflag(self, vflag, val):
        self.vflags[vflag] = val
        self.dirty_vflags.add(vflag)
        self.is_dirty = True
    def change_uflag(self, oldflag, newflag):
        try:
            self.uflags.remove(oldflag)
            self.uflags.add(newflag)
            self.dirty_uflags.add(newflag)
            self.is_dirty = True
        except:
            raise KeyError(f'flag: {oldflag} is not found to change')
    def change_vflag(self, flag, newval):
        try:
            self.vflags[flag] = newval
            self.dirty_vflags.add(flag)
            self.is_dirty = True
        except:
            raise KeyError(f'flag: {flag} is not found to change')
    def remove_uflag(self, flag):
        try:
            self.uflags.remove(flag)
            self.is_dirty = True
        except:
            raise KeyError(f'flag: {flag} is not found to change')
    def remove_vflag(self, flag):
        try:
            del self.vflags[flag]
            self.is_dirty = True
        except:
            raise KeyError(f'flag: {flag} is not found to change')
    def blank_flag(self):
        self.uflags = set()
        self.vflags = {}
        self.dirty_uflags = set()
        self.dirty_vflags = set()
        self.is_dirty = False
def convert(pos, offset):
    return pos[x] + offset[x], pos[y] + offset[y]
def convert_a_lot(widget: Widget):
    X = np.array(widget.pos_x)
    Y = np.array(widget.pos_y)
    result_pos = (X + widget.rect.x, Y + widget.rect.y)
    return result_pos
def createpairpack(Objname,valname1, valname2):
    return namedtuple(Objname, [valname1, valname2])
class PygameRender:
    def __init__(self, widget: Widget, base_screen):
        self.widget = widget
        self.base_screen = base_screen
    def render(self):
        from Kernel.PygameRender.LinkRenderfunc import renderfunc
        for flag in list(self.widget.dirty_vflags):
            if flag in renderfunc:
                renderfunc[flag](self.widget, self.base_screen)
                pygame.display.flip()
class SkiaRender:
    def __init__(self, widget: Widget):
        self.widget = widget
    #coming soon
class UltraRender:
    def __init__(self):
        print('Render with OpenGL coming soon in kernel 2.0')