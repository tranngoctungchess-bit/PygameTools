from typing import Tuple, Union, Dict
from dataclasses import dataclass
import pygame
from pgtkb.KernelPosition import Margin
from pgtkb.ObjType import PosTuple, RectTuple
from pgtkb.RFlags import *
from pgtkb.KernalInit import init
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
w, h: the width and the height of this rect
"""
@dataclass(frozen=True)
class ImmutableRect:
    __slots__ = ('x', 'y', 'w', 'h')
    x:int | float
    y:int |float
    w:int | float
    h:int |float
@dataclass
class MutableRect:
    __slots__ = ('x', 'y', 'w', 'h')
    x:int | float
    y:int |float
    w:int | float
    h:int |float


class Widget:
    """

    """
    __slots__ = ('parent' ,'rect', 'name', 'is_dirty', 'uflags', 'vflags', 'dirty_uflags',
                 'dirty_vflags', 'dirty_auto_flag', 'child',
                 'margin_manager', 'anchor', 'render_engine', 'render_engine_type', 'focused')
    def __init__(self, parent: Union["MainScreen", "Widget"], rect: RectTuple | PosTuple,
                 can_change = False, name: str | None = None):
        if len(rect) == 2:
            w, h = rect
            rect = (0, 0, w, h)
        else:
            if isinstance(parent, Widget):
                x,y,w,h = rect
                rect = (x + parent.rect.x, y +parent.rect.y, w, h)
        self.rect = ImmutableRect(*rect) if not can_change else MutableRect(*rect)
        self.parent = parent
        self.name = name if name else str(id(self))
        self.uflags = set()
        self.vflags = {}
        self.dirty_uflags = set()
        self.dirty_vflags = set()
        self.dirty_auto_flag = set()
        self.child: dict[str, "Widget"] = {}
        if isinstance(parent, (MainScreen, Widget)):
            parent.child[self.name] = self
        self.margin_manager: None | Margin = None
        self.anchor = None
        self.render_engine_type = self.parent.render_engine_type
        if self.parent.render_engine_type:
            self.render_engine = self.parent.render_engine_type(self)
        else:
            self.render_engine = None
        self.focused = False
    def set_render_engine(self, engine):
        self.render_engine = engine(self)
    def render(self):
        self.render_engine.render()
    def get_background(self):
        if isinstance(self.parent, Widget):
            if bg_widget in self.parent.vflags:
                return self.parent.vflags[bg_widget]
            return self.parent.get_background()
        elif isinstance(self.parent, MainScreen):
            return self.parent.background
        else:
            raise ValueError("Your widget parent must be the widget, pygame.Surface or MainScreen class")
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
    def get_pos(self) -> PosTuple:
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
            pygame.draw.rect(surface, bg, (self.rect.x,self.rect.y, self.rect.w, self.rect.h))
        elif isinstance(bg, pygame.Surface):
            surface = self.get_surface()
            surface.blit(bg, (0,0), (self.rect.x,self.rect.y, self.rect.w, self.rect.h))
    def change_rect(self, rect: RectTuple):
        self.change_pos((rect[0], rect[1]))
        self.change_size((rect[2], rect[3]))

    def change_pos(self, new_pos: PosTuple):
        dx = new_pos[0] - self.rect.x
        dy = new_pos[1] - self.rect.y

        if dx == 0 and dy == 0:
            return

        self.rerender()
        if isinstance(self.rect, MutableRect):
            self.rect.x, self.rect.y = new_pos
        else:
            self.rect = ImmutableRect(new_pos[0], new_pos[1], self.rect.w, self.rect.h)

        for chd in self.child.values():
            new_chd_x = chd.rect.x + dx
            new_chd_y = chd.rect.y + dy
            chd.change_pos((new_chd_x, new_chd_y))
    def change_size(self, new_size: PosTuple):
        self.rerender()
        if isinstance(self.rect, MutableRect):
            self.rect.w, self.rect.h = new_size
        else:
            self.rect = ImmutableRect(self.rect.x, self.rect.y, new_size[0], new_size[1])
    def rerender(self):
        self.dirty_vflags.update(self.vflags.keys())
        self.dirty_uflags.update(self.uflags)
        for chd in self.child.values():
            chd.rerender()
        self.hide_itself()
    def inrect(self, pos: PosTuple):
        px, py = pos
        return (self.rect.x <= px <= self.rect.x + self.rect.w) and (self.rect.y <= py <= self.rect.y + self.rect.h)
    def replace_itself(self, new_widget: "Widget"):
        self.name = new_widget.name
        self.uflags = new_widget.uflags.copy()
        self.dirty_uflags = new_widget.dirty_uflags.copy()
        self.vflags = new_widget.vflags.copy()
        self.dirty_vflags = new_widget.dirty_vflags.copy()
        self.dirty_auto_flag = new_widget.dirty_auto_flag
        self.parent.child[self.name] = new_widget
        self.child = new_widget.child
        self.rerender()

    def push_margin(self, anchor, percentage_padding: None | PosTuple = None, padding: None | PosTuple = (0, 0)):
        from pgtkb.KernelPosition import Margin
        self.margin_manager = Margin(self.parent, percentage_padding, padding)
        if self.margin_manager:
            pos_x, pos_y = self.margin_manager.get_pos(self.get_size(), anchor)
            if isinstance(self.parent, Widget):
                pos_x += self.parent.rect.x
                pos_y += self.parent.rect.y
            self.change_pos((pos_x, pos_y))
        self.anchor = anchor
    def set_margin(self, padding, border_percent: PosTuple | None=None):
        from pgtkb.KernelPosition import Margin
        self.margin_manager = Margin(self.parent, border_percent, padding)

    def anchor_to_pos(self, anchor: str):
        if self.margin_manager:
            pos_x, pos_y = self.margin_manager.get_pos(self.get_size(), anchor)
            if isinstance(self.parent, Widget):
                pos_x += self.parent.rect.x
                pos_y += self.parent.rect.y

            self.change_pos((pos_x, pos_y))
        self.anchor = anchor
    def set_flags(self, uflags: tuple=(), vflags: tuple[tuple]=(())):
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

    def dispatch_resize(self):
        if self.margin_manager:
            self.margin_manager.update_on_resize(self.parent)
            if self.anchor:
                self.push_margin(self.anchor, self.margin_manager.percentage, self.margin_manager.padding)
            self.rerender()
        else:
            self.rerender()
        for child in self.child.values():
            if not child.margin_manager:
                child.dispatch_resize()
    def dispatch_click(self, *args):
        return trashfunc
    def dispatch_release(self, *args):
        return trashfunc
    def dispatch_hover(self, *args):
        return trashfunc
def convert(pos, offset):
    return pos[0] + offset[0], pos[1] + offset[1]
def convert_a_lot(widget: Widget):
    offset_x, offset_y = widget.rect.x, widget.rect.y
    new_x = [val + offset_x for val in widget.pos_x]
    new_y = [val + offset_y for val in widget.pos_y]
    return new_x, new_y
class MainScreen:
    """
    """
    def __init__(self, size, flags=0, bg = (0,0,0), fixed = False):
        if fixed:
            self.surface = pygame.display.set_mode(size, flags)
        else:
            self.surface = pygame.display.set_mode(size, pygame.RESIZABLE | flags)
        if valid_background(bg):
            self.background = bg
        self.child = {}
        self.margin_manager = None
        self.blank(bg)
        self.render_engine_type = None
        self.focused = False
    def get_size(self):
        return self.surface.get_size()
    def set_margin(self, padding, border_percent: PosTuple | None= None):
        from pgtkb.KernelPosition import Margin
        self.margin_manager = Margin(self.surface, border_percent, padding)
    def set_caption(self, caption: str):
        pygame.display.set_caption(caption)
    def blank(self, new_bg=None):
        if not new_bg:
            if not isinstance(self.background, pygame.Surface):
                self.surface.fill(self.background)
            else:
                self.blit(self.background, (0,0))
        else:
            if not isinstance(new_bg, pygame.Surface):
                self.surface.fill(new_bg)
            else:
                self.blit(new_bg, (0,0))
    def blit(self, source, dest):
        self.surface.blit(source, dest)
    def blit_to_anchor(self,surface, anchor: str):
        if self.margin_manager:
            pos = self.margin_manager.get_pos(surface.get_size(), anchor)
            self.surface.blit(surface, pos)
        else:
            raise ValueError("you must set the margin manager after blit to anchor")
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
    def set_common_engine(self, engine):
        self.render_engine_type = engine
    def flip(self):
        pygame.display.flip()
class PygameRender:
    """

    """
    def __init__(self, widget: Widget):
        self.widget = widget
        if isinstance(self.widget.parent, Widget):
            self.bg = self.widget.parent.get_background()
        elif isinstance(self.widget.parent, MainScreen):
            self.bg = self.widget.parent.background
        else:
            raise ValueError("Your widget parent must be the widget, pygame.Surface or MainScreen class")
    def render(self):
        from pgtkb.PgRenderCompo.LinkRenderfunc import renderfunc
        try:
            if len(self.widget.uflags) == 0 and len(self.widget.vflags) == 0:
                self.widget.hide_itself()
            else:
                for flag in self.widget.dirty_uflags:
                    renderfunc[flag](self.widget)
                for flag in self.widget.dirty_vflags:
                    renderfunc[flag](self.widget, self.widget.get_surface())
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
