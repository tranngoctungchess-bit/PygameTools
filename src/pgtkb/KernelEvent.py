import pygame
from functools import partial

from pgtkb.KernelWidget import MainScreen
from pgtkb.VFlags import *


def _handle_resize(self: "EventDispatcher"):
    self.screen.handle_resize_bg(self.event.size)
    if self.screen.margin_manager:
        self.screen.margin_manager.update_on_resize(self.screen)
    for widget in self.screen.child.values():
        widget.dispatch_resize()
    self.screen.blank()
    pygame.display.flip()
def _handle_quit(self: "EventDispatcher"):
    return False
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
special_event_to_handle = {
    pygame.VIDEORESIZE: _handle_resize,
    pygame.QUIT: _handle_quit,
}
def extra_parameter(handler, *args, **kwargs):
    return partial(handler, *args, **kwargs)
class EventDispatcher:
    def __init__(self, screen: MainScreen):
        self.screen = screen
        self.current_hovered = None
        self.event = None
        self.focused_widget = set()
        self.pressed_key = set()
    def event_passdown(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.event = event
            match event.type:
                case pygame.MOUSEBUTTONDOWN:
                    self._dispatch_mousebuttondown(mouse_pos, event)
                case pygame.MOUSEBUTTONUP:
                    self._dispatch_mousebuttonup(mouse_pos, event)
                case pygame.VIDEORESIZE | pygame.QUIT:
                    result_func = special_event_to_handle[event.type]
                    is_off = result_func(self)
                    if is_off is False:
                        return False
                case pygame.TEXTINPUT:
                    for widget in self.focused_widget:
                        if hasattr(widget, 'process_addchar'):
                            widget.process_addchar(event.text)
                case pygame.KEYDOWN:
                    self.pressed_key.add(event.key)
                    self._dispatch_key(event)
                case pygame.KEYUP:
                    self.pressed_key.discard(event.key)
        self._dispacth_hover(mouse_pos)
        return True
    def _dispatch_key(self, event):
        match event.key:
            case pygame.K_BACKSPACE:
                if event.scancode == 0:
                    return
                for widget in self.focused_widget:
                    if hasattr(widget, 'process_backspace'):
                        widget.process_backspace()
            case pygame.K_RIGHT:
                for widget in self.focused_widget:
                    if hasattr(widget, 'change_cursor_pos'):
                        widget.change_cursor_pos(1)
            case pygame.K_LEFT:
                for widget in self.focused_widget:
                    if hasattr(widget, 'change_cursor_pos'):
                        widget.change_cursor_pos(-1)
            case pygame.K_RETURN | pygame.K_KP_ENTER:
                for widget in self.focused_widget:
                    if hasattr(widget, 'on_enter'):
                        widget.on_enter()
            case pygame.K_INSERT:
                for widget in self.focused_widget:
                    if hasattr(widget, 'on_insert'):
                        widget.on_insert()
    def _dispacth_hover(self, mouse_pos):
        self.event = None
        new_hovered = None
        for widget in list(reversed(self.screen.child.values())):
            if hasattr(widget, 'is_hovered') and widget.inrect(mouse_pos):
                new_hovered = widget
                break

        if new_hovered != self.current_hovered:
            if self.current_hovered:
                self.current_hovered.dispatch_release(mouse_pos)()
                self.current_hovered.is_hovered = False

            if new_hovered:
                new_hovered.dispatch_hover(mouse_pos)()
                new_hovered.is_hovered = True

            self.current_hovered = new_hovered
    def _dispatch_mousebuttondown(self, mouse_pos, event):
        for widget in list(reversed(self.screen.child.values())):
            if widget.inrect(mouse_pos):
                self.screen.focused = False
                if hasattr(widget, 'dispatch_click'):
                    func = widget.dispatch_click(mouse_pos, event)
                    func()
                return
        self.screen.focused = True
    def _dispatch_mousebuttonup(self, mouse_pos, event):
        if not self.screen.focused:
            for widget in list(reversed(self.screen.child.values())):
                if widget.inrect(mouse_pos):
                    for w in list(self.focused_widget):
                        w.focused = False
                    self.focused_widget.clear()

                    widget.focused = True
                    self.focused_widget.add(widget)
                    if hasattr(widget, 'process_addchar'):
                        pygame.key.start_text_input()
                    else:
                        pygame.key.stop_text_input()
                    if hasattr(widget, 'dispatch_click'):
                        func = widget.dispatch_click(mouse_pos, event)
                        func()

                    return
        else:
            for w in list(self.focused_widget):
                w.focused = False
                if hasattr(w, 'process_addchar'):
                    pygame.key.stop_text_input()
            self.focused_widget.clear()
    def is_key_pressed(self, key_code):
        return key_code in self.pressed_key