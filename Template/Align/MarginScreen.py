from typing import Optional, Tuple
import pygame
#main name: Screen for Margin 1.0
import kernel
class MarginScreen:
    def __init__(self, width: int, height: int, border_percent: Optional[Tuple[float, float]], resizeable = 0):
        self.flags = pygame.RESIZABLE if resizeable else 0
        self.display = pygame.display.set_mode((width, height), flags=self.flags)
        self.margin_manager = kernel.Margin(self.display, padding=border_percent)
        self.width = width
        self.height = height
        self.resizeable = resizeable
    def get_pos(self, obj_size: Optional[Tuple[float, float]], anchor: str):
        return self.margin_manager.get_pos(obj_size, anchor)
    def fill(self, color):
        self.display.fill(color)
    def anchor_render(self, surface: pygame.Surface, anchor: str):
        pos = self.get_pos(surface.get_size(), anchor)
        self.display.blit(surface, pos)
    def update(self):
        pygame.display.flip()
    def resize_screen_handle(self, event):
        if event == pygame.VIDEORESIZE and self.resizeable:
            self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.margin_manager.update_on_resize(self.display)
            self.width, self.height = event.w, event.h
