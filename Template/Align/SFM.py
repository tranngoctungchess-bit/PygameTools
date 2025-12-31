from typing import Optional, Tuple

import pygame
#main name: Screen for Margin 1.0
import kernel
class MarginScreen:
    def __init__(self, width: int, height: int, border_percent: Optional[Tuple[float, float]] ):
        self.display = pygame.display.set_mode((width, height))
        self.margin_manager = kernel.Margin(self.display, padding=border_percent)
        self.width = width
        self.height = height
    def get_pos(self, obj_size: tuple, anchor: str):
        return self.margin_manager.get_pos(obj_size, anchor)
    def fill(self, color):
        self.display.fill(color)
    def anchor_render(self, surface: pygame.Surface, anchor: str):
        pos = self.get_pos(surface.get_size(), anchor)
        self.display.blit(surface, pos)
    def update(self):
        pygame.display.flip()
