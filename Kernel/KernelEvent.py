import pygame
from functools import partial
from Kernel.KernelWidget import MainScreen
from Kernel.VFlags import *
def _handle_resize(self: "EventDispatcher"):
    self.screen.blank()
    for widget in list(reversed(self.screen.child.values())):
        widget.dispatch_resize()
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
    def event_passdown(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type in(pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                for widget in list(reversed(self.screen.child.values())):
                    if widget.inrect(mouse_pos):
                        if hasattr(widget, 'dispatch_click'):
                            func = widget.dispatch_click(mouse_pos, event)
                            func()
                        break
            elif event.type in special_event_to_handle:
                result_func = special_event_to_handle[event.type]
                is_off = result_func(self)
                if is_off is False:
                    return False
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

        return True
