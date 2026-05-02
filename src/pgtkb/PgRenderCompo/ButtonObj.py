from pgtkb import Widget, CircleWidget, valid_background
from pgtkb.VFlags import *
from pgtkb.ObjType import RectTuple, PosTuple
import pygame
from collections import deque
from functools import wraps
def trashfunc(*args, **kwargs):
    pass
class FixedButton(Widget):
    __slots__ = ("is_hovered", "lock_hover", "bg")
    def __init__(self, parent, rect: RectTuple | PosTuple, bg=None, hoverbg=None, pressbg=None,name: str| None = None):
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
        result_func = trashfunc
        from pgtkb.KernelEvent import mouse_event2flags
        for widget in list(reversed(self.child.values())):
            if widget.inwidget(mouse_pos):
                func = widget.dispatch_click(mouse_pos, event)
                result_func = func

        if self.inwidget(mouse_pos):
            self.handle_click_event(event)

            flag = mouse_event2flags.get(event.type, {}).get(event.button)
            return self.get_handler(flag)

        return result_func

    def handle_click_event(self, event):
        if pressed_bg in self.vflags:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.vflags[bg_widget] = self.vflags[pressed_bg]
                self.lock_hover = True
                self.rerender()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.lock_hover = False
                self.add_vflag((bg_widget, self.bg))
                self.rerender()

    def get_handler(self, flag):
        handler = self.vflags.get(flag, trashfunc)
        if handler == trashfunc:
            return trashfunc

        import inspect
        param_count = len(inspect.signature(handler).parameters)

        if param_count == 0:
            return lambda: handler()
        else:
            return lambda: handler(self)

    def handle_realease_visual(self):
        self.vflags[bg_widget] = self.bg
        self.lock_hover = False
        self.rerender()
    def dispatch_hover(self, mouse_pos):
        result_func = trashfunc
        if not hasattr(self, 'text'):
             pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        for widget in list(reversed(self.child.values())):
            if widget.inwidget(mouse_pos):
                func = widget.dispatch_hover(mouse_pos)
                result_func = func
        if self.inwidget(mouse_pos):
            if hover_bg in self.vflags:
                if not self.lock_hover:
                    self.add_vflag((bg_widget, self.vflags[hover_bg]))
                    self.rerender()
            return self.get_handler(Hoverfunc)
        return result_func
    def dispatch_release(self, mouse_pos):
        result_func = trashfunc
        if not hasattr(self, 'text'):
             pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for widget in list(reversed(self.child.values())):
            if not widget.inwidget(mouse_pos):
                func = widget.dispatch_release(mouse_pos)
                result_func = func
        if not self.inwidget(mouse_pos):
            self.handle_realease_visual()
            return self.get_handler(Realeasefunc)
        return result_func
    def on_event(self, flag):
        def decorator(func):
            self.vflags[flag] = func
            self.dirty_vflags.add(flag)
            return func
        return decorator
    def on_dlclick(self):
        return self.on_event(Downlclick)
    def on_drclick(self):
        return self.on_event(Downrclick)
    def on_ulclick(self):
        return self.on_event(Uplclick)
    def on_urclick(self):
        return self.on_event(Uprclick)
    def on_dsmouse(self):
        return self.on_event(Downscrollmouse)
    def on_usmouse(self):
        return self.on_event(Upscrollmouse)
    def on_hover(self):
        return self.on_event(Hoverfunc)
    def on_release(self):
        return self.on_event(Realeasefunc)

class CircleButton(CircleWidget):
    __slots__ = ("is_hovered", "lock_hover", "bg")
    def __init__(self, parent, center_pos, radius, bg=None, hoverbg=None, pressbg=None, name: str| None = None):
        super().__init__(center_pos, radius, parent, name=name)
        self.is_hovered = False
        self.lock_hover = False
        if valid_background(bg):
            self.add_vflag((bg_widget, bg))
        self.bg = bg
        if valid_background(hoverbg):
            self.add_vflag((hover_bg, hoverbg))
        if valid_background(pressbg):
            self.add_vflag((pressed_bg, pressbg))

    set_hoverbg = FixedButton.set_hoverbg
    set_pressbg = FixedButton.set_pressbg
    set_disablebg = FixedButton.set_disablebg
    dispatch_click = FixedButton.dispatch_click
    handle_click_event = FixedButton.handle_click_event
    get_handler = FixedButton.get_handler
    handle_realease_visual = FixedButton.handle_realease_visual
    dispatch_hover = FixedButton.dispatch_hover
    dispatch_release = FixedButton.dispatch_release
    on_event = FixedButton.on_event
    on_dlclick = FixedButton.on_dlclick
    on_drclick = FixedButton.on_drclick
    on_ulclick = FixedButton.on_ulclick
    on_urclick = FixedButton.on_urclick
    on_dsmouse = FixedButton.on_dsmouse
    on_usmouse = FixedButton.on_usmouse
    on_hover = FixedButton.on_hover
    on_release = FixedButton.on_release

class ToggleButton(FixedButton):
    def __init__(self, parent, rect,name: str| None = None, fbg=None, tbg=None, hoverbg=None, lock_toogle=False):
        super().__init__(parent, rect, fbg, hoverbg, tbg, name=name)
        self.lock_toogle = lock_toogle
        self.state = False
        self.group = None

    def handle_click_event(self, event):
        if self.lock_toogle: return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                next_visual = not self.state
                self.vflags[bg_widget] = self.vflags[pressed_bg] if next_visual else self.bg
                self.lock_hover = True
                self.rerender()
            case pygame.MOUSEBUTTONUP:
                if self.group:
                    if not self.state:
                        self.state = self.group.handle_request_on(self)
                    else:
                        self.state = False
                        self.group.handle_request_off(self)
                else:
                    self.state = not self.state

                self.lock_hover = self.state
                self.vflags[bg_widget] = self.vflags[pressed_bg] if self.state else self.bg
                self.rerender()

    def handle_realease_visual(self):
        if self.state:
            self.vflags[bg_widget] = self.vflags.get(pressed_bg, self.bg)
            self.lock_hover = True
        else:
            self.vflags[bg_widget] = self.bg
            self.lock_hover = False
        self.rerender()
class CircleToogleButton(CircleButton):
    def __init__(self, parent,center_pos, radius ,name: str| None = None, fbg=None, tbg=None, hoverbg=None, lock_toogle=False):
        super().__init__(parent,center_pos, radius, fbg, hoverbg, tbg, name=name)
        self.lock_toogle = lock_toogle
        self.state = False
        self.group = None
    def handle_click_event(self, event):
        if self.lock_toogle: return
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                next_visual = not self.state
                self.vflags[bg_widget] = self.vflags[pressed_bg] if next_visual else self.bg
                self.lock_hover = True
                self.rerender()
            case pygame.MOUSEBUTTONUP:
                if self.group:
                    if not self.state:
                        self.state = self.group.handle_request_on(self)
                    else:
                        self.state = False
                        self.group.handle_request_off(self)
                else:
                    self.state = not self.state

                self.lock_hover = self.state
                self.vflags[bg_widget] = self.vflags[pressed_bg] if self.state else self.bg
                self.rerender()

    def handle_realease_visual(self):
        if self.state:
            self.vflags[bg_widget] = self.vflags.get(pressed_bg, self.bg)
            self.lock_hover = True
        else:
            self.vflags[bg_widget] = self.bg
            self.lock_hover = False
        self.rerender()
class ToogleGroup:
    def __init__(self, group: list = None, max_button=1):
        self.group = group if group else []
        self.on_group = deque()
        self.max_button = max_button

        if self.group:
            for btn in self.group:
                btn.group = self

    def add(self, tooglebutton: ToggleButton):
        self.group.append(tooglebutton)
        tooglebutton.group = self

    def remove(self, tooglebutton: ToggleButton):
        if tooglebutton in self.group:
            self.group.remove(tooglebutton)
            tooglebutton.group = None
            if tooglebutton in self.on_group:
                self.on_group.remove(tooglebutton)

    def handle_request_on(self, btn) -> bool:
        if btn not in self.on_group:
            self.on_group.append(btn)
        while len(self.on_group) > self.max_button:
            oldest_btn = self.on_group.popleft()
            oldest_btn.state = False
            oldest_btn.handle_realease_visual()

        return True  # Cho phép bật

    def handle_request_off(self, btn):
        if btn in self.on_group:
            self.on_group.remove(btn)

    def clear(self, turn_off: bool = False):
        for btn in self.group:
            btn.group = None
            if turn_off:
                btn.state = False
                btn.handle_realease_visual()
        self.group.clear()
        self.on_group.clear()

    def change_max(self, new_max: int):
        self.max_button = new_max
        while len(self.on_group) > self.max_button:
            btn = self.on_group.popleft()
            btn.state = False
            btn.handle_realease_visual()