import pygame
from functools import partial
from Kernel.Flags.VFlags import *
event2flags = {
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
    from Kernel.KernelWidget import MainScreen
    def __init__(self, screen: MainScreen):
        self.screen = screen
    def event_passdown(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type in( pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                for widget in list(reversed(self.screen.child.values())):
                    if widget.inrect(mouse_pos):
                        func = widget.dispatch_click(mouse_pos, event)
                        func()
                        break
            elif event.type == pygame.QUIT:
                return False
            for widget in list(reversed(self.screen.child.values())):
                if widget.inrect(mouse_pos) and hasattr(widget, 'is_hovered'):
                    func = widget.dispatch_hover(mouse_pos)
                    func()
                    widget.is_hovered = True
                    break
                else:
                    if widget.is_hovered:
                        func = widget.dispatch_realease(mouse_pos)
                        func()
                        widget.is_hovered = False
        return True


