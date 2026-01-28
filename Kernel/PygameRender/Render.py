import pygame
from Kernel.VFlags import *
from Kernel.UFlags import *
from Kernel.KernelWidget import Widget
from Kernel.ObjType import *
def fill_bg(widget: Widget, screen):
    col = widget.vflags[bg_color]
    pygame.draw.rect(screen,col, widget.get_rect())
    widget.dirty_vflags.remove(bg_color)
def set_border(widget: Widget, screen):
    valpack = widget.vflags[border]
    if corner_radius in widget.vflags:
        pygame.draw.rect(screen, valpack.border_col, widget.get_rect(), valpack.border_width, widget.vflags[corner_radius])
    else:
        pygame.draw.rect(screen, valpack.border_col, widget.get_rect(), valpack.border_width)
    widget.dirty_vflags.remove(border)
    widget.dirty_vflags.remove(corner_radius)
def draw_text(widget: Widget, screen):
    valpack: TextPack = widget.vflags[textpack]
    font = pygame.font.SysFont(valpack.Font, valpack.Size, text_Is_Bold in widget.uflags, text_Is_Italic in widget.uflags)
    if text_Is_Underline in widget.uflags:
        font.set_underline(True)
        widget.dirty_uflags.remove(text_Is_Underline)
    if text_Is_Strikethrough in widget.uflags:
        font.set_strikethrough(True)
        widget.dirty_uflags.remove(text_Is_strikethrough)
    if text_have_background in widget.uflags:
        if bg_color in widget.vflags:
            bg = widget.vflags[bg_color]
        else:
            raise ValueError('Background color is not found')
    else:
        bg = None
    text_surface = font.render(valpack.Text, text_Is_Antialias in widget.uflags, valpack.Color, bg)
    screen.blit(text_surface, widget.get_pos())
    widget.dirty_vflags.remove(textpack)
    if text_Is_Bold in widget.dirty_uflags:
        widget.dirty_uflags.remove(text_Is_Bold)
    if text_Is_Antialias in widget.dirty_uflags:
        widget.dirty_uflags.remove(text_Is_Antialias)
    if text_Is_Italic in widget.dirty_uflags:
        widget.dirty_uflags.remove(text_Is_Italic)