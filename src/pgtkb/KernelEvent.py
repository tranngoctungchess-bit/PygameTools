import pygame
from functools import partial
from pgtkb.KernelWidget import MainScreen
from pgtkb.VFlags import *
def _truecallback(funcs: tuple):
    for func in funcs:
        res = func()
        if res is False:
            return res
    return True
mouse_event2flags = {
    pygame.MOUSEBUTTONUP : {
        1: Uplclick,
        2: Upscrollmouse,
        3: Uprclick,
        4: Upscrollup,
        5: Upscrolldown,
    },
    pygame.MOUSEBUTTONDOWN : {
        1 : Downlclick,
        2 : Downscrollmouse,
        3 : Downrclick,
        4 : Downscrollup,
        5 : Downscrolldown,
    }
}
def extra_parameter(handler, *args, **kwargs):
    return partial(handler, *args, **kwargs)
class EventDispatcher:
    def __init__(self, screen: MainScreen):
        self.screen = screen
        self.current_hovered = None
        self.event = None
        self.focused_obj = set()
        self.pressed_key = set()
        self.mouse_pos = None
        self.dispatching_mods = {}
        self.dispatching_events = {
            pygame.QUIT: [self._dispatch_quit],
            pygame.VIDEORESIZE: [self._dispatch_resize],
            pygame.MOUSEBUTTONDOWN: [self._dispatch_mousebuttondown],
            pygame.MOUSEBUTTONUP: [self._dispatch_mousebuttonup],
            pygame.KEYDOWN: [self._dispatch_keydown],
            pygame.KEYUP: [self._dispatch_keyup],
            pygame.TEXTINPUT: [self._dispatch_textinput],
        }

        self.dispatching_keys = {
            pygame.K_LEFT: [self._dispatch_keyleft],
            pygame.K_RIGHT: [self._dispatch_keyright],
            pygame.K_BACKSPACE: [self._dispatch_backspace],
            pygame.K_INSERT: [self._dispatch_insert],
            pygame.K_RETURN: [self._dispatch_enter],
            pygame.K_KP_ENTER: [self._dispatch_enter],
        }
    def event_passdown(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.event = event
            if self.event.type in self.dispatching_events:
                func_list = self.dispatching_events[self.event.type]
                res = _truecallback(func_list)
                if not res: return res
        self._dispatch_hover()
        return True
    def _dispatch_keydown(self):
        if hasattr(self.event, 'mod') and self.event.mod:
            for mods, key_dict in self.dispatching_mods.items():
                if all(self.event.mod & m for m in mods):
                    if self.event.unicode != '':
                        funcs = key_dict.get(self.event.key)
                    else:
                        funcs = key_dict.get(())
                    if funcs:
                        _truecallback(funcs)
                        return
        if self.event.key in self.dispatching_keys:
            func_list = self.dispatching_keys[self.event.key]
            _truecallback(func_list)
    def _dispatch_mousebuttondown(self):
        for widget in list(reversed(self.screen.child.values())):
            if widget.inwidget(self.mouse_pos):
                self.screen.focused = False
                if hasattr(widget, 'dispatch_click'):
                    func = widget.dispatch_click(self.mouse_pos, self.event)
                    func()
                return
        self.screen.focused = True

    def _dispatch_mousebuttonup(self):
        if not self.screen.focused:
            for widget in list(reversed(self.screen.child.values())):
                if widget.inwidget(self.mouse_pos):
                    for w in list(self.focused_obj):
                        w.focused = False
                    self.focused_obj.clear()

                    widget.focused = True
                    self.focused_obj.add(widget)
                    if hasattr(widget, 'process_addchar'):
                        pygame.key.start_text_input()
                    else:
                        pygame.key.stop_text_input()
                    if hasattr(widget, 'dispatch_click'):
                        func = widget.dispatch_click(self.mouse_pos, self.event)
                        func()

                    return
        else:
            for w in list(self.focused_obj):
                w.focused = False
                if hasattr(w, 'process_addchar'):
                    pygame.key.stop_text_input()
            self.focused_obj.clear()
    def _dispatch_quit(self):
        return False
    def _dispatch_resize(self):
        self.screen.handle_resize_bg(self.event.size)
        if self.screen.margin_manager:
            self.screen.margin_manager.update_on_resize(self.screen)
        for widget in self.screen.child.values():
            widget.dispatch_resize()
        self.screen.blank()
        pygame.display.flip()
    def _dispatch_keyleft(self):
        for widget in self.focused_obj:
            if hasattr(widget, 'change_cursor_pos'):
                widget.change_cursor_pos(-1)
    def _dispatch_keyright(self):
        for widget in self.focused_obj:
            if hasattr(widget, 'change_cursor_pos'):
                widget.change_cursor_pos(1)
    def _dispatch_insert(self):
        for widget in self.focused_obj:
            if hasattr(widget, 'on_insert'):
                widget.on_insert()
    def _dispatch_backspace(self):
        if self.event.scancode == 0:
            return
        for widget in self.focused_obj:
            if hasattr(widget, 'process_backspace'):
                widget.process_backspace()
    def _dispatch_textinput(self):
        for widget in self.focused_obj:
            if hasattr(widget, 'process_addchar'):
                widget.process_addchar(self.event.text)
    def _dispatch_enter(self):
        for widget in self.focused_obj:
            if hasattr(widget, 'dispatch_enter'):
                widget.dispatch_enter()
    def _dispatch_keyup(self):
        self.pressed_key.discard(self.event.key)
    def _dispatch_hover(self):
        self.event = None
        new_hovered = None
        for widget in list(reversed(self.screen.child.values())):
            if hasattr(widget, 'is_hovered') and widget.inwidget(self.mouse_pos):
                new_hovered = widget
                break

        if new_hovered != self.current_hovered:
            if self.current_hovered:
                self.current_hovered.dispatch_release(self.mouse_pos)()
                self.current_hovered.is_hovered = False

            if new_hovered:
                new_hovered.dispatch_hover(self.mouse_pos)()
                new_hovered.is_hovered = True

            self.current_hovered = new_hovered
    def add_efunc(self, event, func):
        if dispatching_events[event]:
            self.dispatching_events[event].append(func)
        else:
            self.dispatching_keys[event] = [func]
    def add_kfunc(self,key, func):
        if self.dispatching_keys[key]:
            self.dispatching_keys[key].append(func)
        else:
            self.dispatching_keys[key] = [func]
    def add_kmod_func(self, mods, key=(), func=None):
        if not isinstance(mods, tuple):
            mods = (mods,)
        if mods not in self.dispatching_mods:
            self.dispatching_mods[mods] = {}
        if key not in self.dispatching_mods[mods]:
            self.dispatching_mods[mods][key] = []
        if func:
            self.dispatching_mods[mods][key].append(func)
    def check_combokey(self, mods, key):
        if not isinstance(mods, (tuple, list)):
            mods = (mods,)
        return all(self.event.mod & mod for mod in mods) and self.event.key == key
    def new_event(self, event, func):
        self.dispatching_events[event] = func
    def new_key(self, key, func):
        self.dispatching_keys[key] = func
    def is_key_pressed(self, key_code):
        return key_code in self.pressed_key