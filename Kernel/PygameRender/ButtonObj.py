from typing import Tuple
from Kernel import Widget, valid_background, Downrclick, PygameRender
from Kernel.Flags.VFlags import *
from Kernel.ObjType import MathVal1, MathVal2
import pygame
def trashfunc(*args, **kwargs):
    pass
class FixedButton(Widget):
    def __init__(self, parent,name,  rect: MathVal1 | MathVal2, bg=None, hoverbg=None, pressbg=None):
        super().__init__(parent, rect=rect, name=name)
        self.is_hovered = False
        self.lock_hover = False
        if valid_background(bg):
            self.add_vflag((bg_widget, bg))
        self.bg = bg
        if valid_background(hoverbg):
            self.add_vflag((hover_bg, hoverbg))
        if valid_background(pressbg):
            self.add_vflag((pressed_bg, pressbg))
    def set_hoverbg(self, hoverbg):
        if valid_background(hoverbg):
            self.add_vflag((hover_bg, hoverbg))
    def set_pressbg(self, pressbg):
        if valid_background(pressbg):
            self.add_vflag((press_bg, pressbg))
    def set_disablebg(self, disablebg):
        if valid_background(disablebg):
            self.add_vflag((disable_bg, disablebg))
    def dispatch_click(self, mouse_pos, event):
        from Kernel.KernelEvent import mouse_event2flags
        for widget in list(reversed(self.child.values())):
            if widget.inrect(mouse_pos):
                func = widget.dispatch_click(mouse_pos, event)
                if func:
                    return func
        if self.inrect(mouse_pos):
            if pressed_bg in self.vflags:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.vflags[bg_widget] = self.vflags[pressed_bg]
                    self.lock_hover = True
                    self.rerender()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.lock_hover = False
                    self.add_vflag((bg_widget, self.bg))
                    self.rerender()
            flag = mouse_event2flags.get(event.type, {}).get(event.button)
            handler = self.vflags.get(flag, trashfunc)
            if handler != trashfunc:
                import inspect
                param_count = len(inspect.signature(handler).parameters)

                if param_count == 0:
                    return lambda: handler()
                else:
                    return lambda: handler(self)

        return trashfunc
    def dispatch_hover(self, mouse_pos):
        for widget in list(reversed(self.child.values())):
            if widget.inrect(mouse_pos):
                func = widget.dispatch_hover(mouse_pos)
                if func:
                    return func
        if self.inrect(mouse_pos):
            if hover_bg in self.vflags:
                if not self.lock_hover:
                    self.add_vflag((bg_widget, self.vflags[hover_bg]))
                    self.rerender()
            handler = self.vflags.get(Hoverfunc, trashfunc)
            if handler != trashfunc:
                import inspect
                param_count = len(inspect.signature(handler).parameters)

                if param_count == 0:
                    return lambda: handler()
                else:
                    return lambda: handler(self)

        return trashfunc
    def dispatch_release(self, mouse_pos):
        for widget in list(reversed(self.child.values())):
            if not widget.inrect(mouse_pos):
                func = widget.dispatch_release(mouse_pos)
                if func:
                    return func
        if not self.inrect(mouse_pos):
            self.vflags[bg_widget] = self.bg
            self.lock_hover = False
            self.rerender()
            handler = self.vflags.get(Realeasefunc, trashfunc)
            if handler != trashfunc:
                import inspect
                param_count = len(inspect.signature(handler).parameters)

                if param_count == 0:
                    return lambda: handler()
                else:
                    return lambda: handler(self)

        return trashfunc