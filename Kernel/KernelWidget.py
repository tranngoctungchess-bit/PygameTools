from typing import Tuple, Union
from dataclasses import dataclass
from collections import namedtuple
import pygame
import array

import Kernel.KernelPosition
from Kernel import Margin
from Kernel.KernalInit import should_fill, set_fill_mode
from Kernel.ObjType import MathVal2, MathVal1
from Kernel.Flags.RFlags import rflags_to_uflags, rflags_to_vflags
from Kernel.KernalInit import init
init()
def trashfunc(*args, **kwargs):
    pass
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
    __slots__ = ('parent' ,'rect', 'is_dirty', 'uflags', 'vflags', 'dirty_uflags', 'dirty_vflags', 'dirty_auto_flag','pos_x', 'pos_y', 'temp_bg', 'child')
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
        self.child = {}
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
        self.child[name] = widget
    def destroy(self):
        self.hide_itself()
        if isinstance(self.parent, Widget):
            for name, child in self.parent.child.items():
                if child is self:
                    del self.parent.child[name]
                    break
        self.parent = None
        self.child.clear()
    def hide_itself(self):
        bg = self.get_background()
        if isinstance(bg, tuple):
            surface = self.get_surface()
            pygame.draw.rect(surface, bg, (self.rect.x,self.rect.y, self.rect.w, self.rect.y))
        elif isinstance(bg, pygame.Surface):
            surface = self.get_surface()
            surface.blit(bg, self.rect.topleft, self.rect)
    def change_rect(self, rect: MathVal1):
        self.change_pos((rect[0], rect[1]))
        self.change_size((rect[2], rect[3]))
    def change_pos(self, new_pos: MathVal2):
        self.rerender()
        if isinstance(self.rect, MutableRect):
            self.rect.x, self.rect.y = new_pos
            convert_a_lot(self)
        else:
            raise TypeError('Your widget pos and size is immutabe')
    def change_size(self, new_size: MathVal2):
        self.rerender()
        if isinstance(self.rect, MutableRect):
            self.rect.w, self.rect.h = new_size
        else:
            raise TypeError('Your widget pos and size is immutabe')
    def rerender(self):
        self.hide_itself()
        self.dirty_vflags.update(self.vflags.keys())
        self.dirty_uflags.update(self.uflags)
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
    def add_uflag(self, *uflags):
        for uflag in uflags:
            self.uflags.add(uflag)
            self.dirty_uflags.add(uflag)
    def add_vflag(self, *flagpacks):
        for flagpack in flagpacks:
            vflag, val = flagpack
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
    def dispatch_mouse(self, mouse_pos, event):
        from Kernel.KernelEvent import event2flags
        for widget in list(reversed(self.child.values())):
            if widget.inrect(mouse_pos):
                func = widget.dispatch_mouse(mouse_pos, event)
                if func:
                    return func
        if self.inrect(mouse_pos):
            flag = event2flags.get(event.type, {}).get(event.button)
            handler = self.vflags.get(flag, trashfunc)
            if handler != trashfunc:
                import inspect
                param_count = len(inspect.signature(handler).parameters)

                if param_count == 0:
                    return lambda: handler()
                else:
                    return lambda: handler(self)

        return trashfunc
def convert(pos, offset):
    return pos[0] + offset[0], pos[1] + offset[1]
def convert_a_lot(widget: Widget):
    X = array.array('f', widget.pos_x)
    Y = array.array('f', widget.pos_y)
    offset_x, offset_y = widget.rect.x, widget.rect.y
    for i in range(len(X)):
        X[i] += offset_x
        Y[i] += offset_y
    return X, Y
class MainScreen:
    """
    """
    def __init__(self, size, flags=0):
        self.surface = pygame.display.set_mode(size, flags)
        self.background = (0,0,0)
        self.child = {}
        self.margin_manager = None
    def set_margin(self, border_percent: MathVal2 | None, padding):
        from Kernel.KernelPosition import Margin
        self.margin_manager = Margin(self.surface, border_percent, padding)
    def fill(self, color):
        if should_fill():
            self.surface.fill(color)
        self.background = color
    def blank(self, color):
        self.surface.fill(color)
    def blit(self, source, dest):
        self.surface.blit(source, dest)
    def blit_to_anchor(self, surface, anchor: str):
        pos = self.surface.get_pos(surface.get_size(), anchor)
        self.surface.blit(surface, pos)
    def addWidget(self, widget: Widget, widget_id):
        self.child[widget_id] = widget
    def delWidget(self, widget_id):
        del self.child[widget_id]
    def getWidget(self, widget_id: str) -> Widget:
        return self.child.get(widget_id)
    def clearWidget(self):
        for widget in self.child.values():
            widget.destroy()
        self.child.clear()
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