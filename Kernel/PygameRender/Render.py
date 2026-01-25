import pygame
from Kernel.VFlags import *
from Kernel.KernelWidget import Widget
from Kernel.ObjType import *
def fill_bg(widget: Widget, screen):
    col = widget.vflags[bg_color]
    pygame.draw.rect(screen,col, widget.get_rect())
    widget.dirty_vflags.remove(bg_color)
def set_border(widget: Widget, screen):
    valpack = widget.vflags[border]
    print(valpack)
    bg_col = valpack.border_col
    bg_width = valpack.border_width
    print(bg_col, bg_width)
    pygame.draw.rect(screen, bg_col, widget.get_rect(), bg_width)
    widget.dirty_vflags.remove(border)