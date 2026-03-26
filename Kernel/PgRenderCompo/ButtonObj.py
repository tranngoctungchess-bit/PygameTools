from Kernel import Widget, valid_background
from Kernel.VFlags import *
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
        #dispatch recursion
        from Kernel.KernelEvent import mouse_event2flags
        for widget in list(reversed(self.child.values())):
            if widget.inrect(mouse_pos):
                func = widget.dispatch_click(mouse_pos, event)
                if func:
                    return func

        if self.inrect(mouse_pos):
            self._handle_click_event(event)

            flag = mouse_event2flags.get(event.type, {}).get(event.button)
            return self._get_handler(flag)

        return trashfunc

    def _handle_click_event(self, event):
        if pressed_bg in self.vflags:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.vflags[bg_widget] = self.vflags[pressed_bg]
                self.lock_hover = True
                self.rerender()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.lock_hover = False
                self.add_vflag((bg_widget, self.bg))
                self.rerender()

    def _get_handler(self, flag):
        handler = self.vflags.get(flag, trashfunc)
        if handler == trashfunc:
            return trashfunc

        import inspect
        param_count = len(inspect.signature(handler).parameters)

        if param_count == 0:
            return lambda: handler()
        else:
            return lambda: handler(self)

    def _handle_release_visual(self):
        self.vflags[bg_widget] = self.bg
        self.lock_hover = False
        self.rerender()
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
            return self._get_handler(Hoverfunc)
        return trashfunc
    def dispatch_release(self, mouse_pos):
        for widget in list(reversed(self.child.values())):
            if not widget.inrect(mouse_pos):
                func = widget.dispatch_release(mouse_pos)
                if func:
                    return func
        if not self.inrect(mouse_pos):
            self._handle_release_visual()
            return self._get_handler(Realeasefunc)
        return trashfunc
class ToggleButton(FixedButton):
    def __init__(self, parent,name,  rect: MathVal1 | MathVal2, fbg=None, tbg=None, hoverbg=None, lock_toogle=False):
        #tbg and fbg are TrueStateBg and FalseStateBg respectively
        super().__init__(parent, name, rect, fbg, hoverbg, tbg)
        self.lock_toogle = lock_toogle
        self.state = False
    def _handle_click_event(self, event):
        if self.lock_toogle: return
        if pressed_bg in self.vflags:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.vflags[bg_widget] = self.vflags[pressed_bg] if not self.state else self.bg
                self.lock_hover = True
                self.rerender()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.state = not self.state
                self.lock_hover = self.state
                self.vflags[bg_widget] = self.vflags[pressed_bg] if self.state else self.bg
                self.rerender()
    def _handle_release_visual(self):
        if self.state:
            self.vflags[bg_widget] = self.vflags.get(pressed_bg, self.bg)
            self.lock_hover = True
        else:
            self.vflags[bg_widget] = self.bg
            self.lock_hover = False

        self.rerender()