import numpy as np
from typing import Tuple, Union, Optional, List, Dict, Any
from dataclasses import dataclass
from collections import namedtuple
import pygame
from Kernel.ObjType import MathVal2, MathVal1
from Kernel.RFlags import rflags_to_uflags, rflags_to_vflags
from Kernel.UFlags import *
from Kernel.VFlags import *
def valid_background(bg):
    """
    Check if it is a valid background
    """
    if isinstance(bg, pygame.Surface) or (
            isinstance(bg, tuple) and len(bg) in (3, 4) and all(isinstance(x, (int, float)) for x in bg)):
        return True
    else:
        return False
"""
ImmutableRect and MutableRect:
the base object for any widget class as bar, button coming soon in this tool
x, y: the pos of rect
width, height: the width and the height of this rect
"""
ImmutableRect = namedtuple('Rect', ['x', 'y', 'w', 'h'])
Position = namedtuple('Pos', ['x', 'y']) #create to look code easier
@dataclass
class MutableRect:
    __slots__ = ('x', 'y', 'w', 'h')
    x:Union[int, float]
    y:Union[int,float]
    w:Union[int, float]
    h:Union[int,float]
class MainScreen:
    """

    """
    def __init__(self, size, flags=0):
        self.surface = pygame.display.set_mode(size, flags)
        self.background = (0,0,0)
    def fill(self, color):
        self.surface.fill(color)
        self.background = color
    def blit(self, source, dest):
        self.surface.blit(source, dest)
class Widget:
    """
    parent: the base contains this widget
    rect: the rect of this widget
    is_dirty: whether this widget is changed
    uflags: the unchangeable flags set for this widget
    vflags: the changeable flags dict for this widget
    dirty_uflags: the unvalueable flags set for this widget
    dirty_vflags: the valueable flags set for this widget
    pos_x: the x positions list for all objects in this widget
    pos_y: the y positions list for all objects in this widget
    temp_bg: the bg of widget parent, if widget parent is pygame.Surface
    child: the dictionary of widget child
    """
    __slots__ = ('parent' ,'rect', 'is_dirty', 'uflags', 'vflags', 'dirty_uflags', 'dirty_vflags', 'dirty_auto_flag','pos_x', 'pos_y', 'temp_bg', 'children')
    def __init__(self, parent, rect: MathVal1, bg=None, can_change = False):
        self.rect = ImmutableRect(*rect) if not can_change else MutableRect(*rect)
        self.parent = parent
        self.uflags = set()
        self.vflags = {}
        self.dirty_uflags = set()
        self.dirty_vflags = set()
        self.dirty_auto_flag = set()
        self.pos_x = []
        self.pos_y = []
        self.children = {}
        if bg is not None and not valid_background(bg):
            raise ValueError("Invalid background format")
        self.temp_bg = bg
    def get_background(self):
        if isinstance(self.parent, Widget):
            return self.parent.get_background()
        elif isinstance(self.parent, pygame.Surface):
            if self.temp_bg is None:
                raise ValueError("Widget with pygame.Surface parent must provide bg color in __init__")
            return self.temp_bg
        elif isinstance(self.parent, MainScreen):
            return self.parent.background
        else:
            raise ValueError("Your widget parent must be the widget, pygame.Surface or MainScreen class")
    def add_obj(self, pos: MathVal2):
        self.pos_x.append(pos[0])
        self.pos_y.append(pos[1])
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
    def get_pos(self):
        return self.rect.x, self.rect.y
    def get_size(self):
        return self.rect.w, self.rect.h
    def get_surface(self):
        if isinstance(self.parent, pygame.Surface):
            return self.parent
        elif isinstance(self.parent, MainScreen):
            return self.parent.surface
        else:
            return self.parent.get_surface()
    def add_child(self, widget, name):
        self.children[name] = widget
    def destroy(self):
        self.hide_itself()
        if isinstance(self.parent, Widget):
            for name, child in self.parent.children.items():
                if child is self:
                    del self.parent.children[name]
                    break
        self.parent = None
        self.children.clear()
    def hide_itself(self):
        bg = self.get_background()
        if isinstance(bg, tuple):
            surface = self.get_surface()
            pygame.draw.rect(surface, bg, (self.rect.x,self.rect.y, self.rect.w, self.rect.y))
        elif isinstance(bg, pygame.Surface):
            surface = self.get_surface()
            surface.blit(bg, self.rect.topleft, self.rect)
    def inrect(self, pos: MathVal2):
        px, py = pos
        return (self.rect.x <= px <= self.rect.x + self.rect.w) and (self.rect.y <= py <= self.rect.y + self.rect.h)
    def set_flags(self, uflags: tuple=(), vflags: Tuple[tuple]=(())):
        for uflag in uflags:
            self.uflags.add(uflag)
            self.dirty_uflags.add(uflag)
        for pack in vflags:
            self.vflags[pack[0]] = pack[1]
            self.dirty_vflags.add(pack[0])
    def add_uflag(self, uflag):
        self.uflags.add(uflag)
        self.dirty_uflags.add(uflag)
    def add_vflag(self, vflag, val):
        self.vflags[vflag] = val
        self.dirty_vflags.add(vflag)
    def change_uflag(self, oldflag, newflag):
        try:
            self.uflags.remove(oldflag)
            self.uflags.add(newflag)
            self.dirty_uflags.add(newflag)
        except:
            raise KeyError(f'flag: {oldflag} is not found to change')
    def change_vflag(self, flag, newval):
        try:
            self.vflags[flag] = newval
            self.dirty_vflags.add(flag)
        except:
            raise KeyError(f'flag: {flag} is not found to change')
    def remove_uflag(self, flag):
        try:
            rflag = rflags_to_uflags[flag]
            self.uflags.remove(flag)
            self.dirty_vflags.add(rflag)
        except KeyError:
            raise KeyError(f'flag: {flag} is not found to change')
    def remove_vflag(self, flag):
        try:
            rflag = rflags_to_vflags[flag]
            del self.vflags[flag]
            self.dirty_vflags.add(rflag)
        except:
            raise KeyError(f'flag: {flag} is not found to change')
    def blank_flag(self):
        self.uflags = set()
        self.vflags = {}
        self.dirty_uflags = set()
        self.dirty_vflags = set()
def convert(pos, offset):
    return pos[0] + offset[0], pos[1] + offset[1]
def convert_a_lot(widget: Widget):
    X = np.array(widget.pos_x)
    Y = np.array(widget.pos_y)
    result_pos = (X + widget.rect.x, Y + widget.rect.y)
    return result_pos
class PygameRender:
    """

    """
    def __init__(self, widget: Widget):
        self.widget = widget
        if isinstance(self.widget.parent, Widget):
            self.bg = self.widget.parent.get_background()
        elif isinstance(self.widget.parent, pygame.Surface):
            self.bg = self.widget.temp_bg
        elif isinstance(self.widget.parent, MainScreen):
            self.bg = self.widget.parent.background
        else:
            raise ValueError("Your widget parent must be the widget, pygame.Surface or MainScreen class")
    def render(self):
        from Kernel.PygameRender.LinkRenderfunc import renderfunc
        try:
            if len(self.widget.uflags) == 0 and len(self.widget.vflags) == 0:
                self.widget.hide_itself()
            else:
                for flag in self.widget.dirty_uflags:
                    renderfunc[flag](self.widget)
                for flag in self.widget.dirty_vflags:
                    renderfunc[flag](self.widget, self.widget.get_surface())
                    pygame.display.flip()
                for flag in self.widget.dirty_auto_flag:
                    try:
                        renderfunc[flag](self.widget, self.widget.get_surface())
                    except TypeError:
                        renderfunc[flag](self.widget)
            self.widget.dirty_vflags.clear()
            self.widget.dirty_uflags.clear()
            self.widget.dirty_auto_flag.clear()
        except KeyError as e:
            raise ValueError(f"Flag {e} not found in renderfunc mapping. Check LinkRenderfunc.py")
class SkiaRender:
    def __init__(self, widget: Widget):
        self.widget = widget
    #coming soon
class UltraRender:
    def __init__(self):
        print('Render with OpenGL coming soon in kernel 2.0')