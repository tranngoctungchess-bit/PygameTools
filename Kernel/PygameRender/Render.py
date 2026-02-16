import pygame

from Kernel.Flags.VFlags import *
from Kernel.Flags.UFlags import *
from Kernel.KernelWidget import Widget, MainScreen
from Kernel.PygameRender.Textobj import Label

"""
Surface
"""
def fill_bg(widget: Widget, screen: pygame.Surface):
    bg = widget.vflags[bg_widget]
    if isinstance(bg, tuple):
        pygame.draw.rect(screen, bg, (widget.rect.x, widget.rect.y, widget.rect.w, widget.rect.h))
    elif isinstance(bg, pygame.Surface):
        size = bg.get_size()
        if size[0] != widget.rect.w or size[1] != widget.rect.h:
            bg = pygame.transform.scale(bg, (widget.rect.w, widget.rect.h))
        screen.blit(bg, (widget.rect.x,widget.rect.y))
def set_border(widget: Widget, screen):
    valpack = widget.vflags[border]
    if corner_radius in widget.vflags:
        pygame.draw.rect(screen, valpack.border_col, widget.get_rect(), valpack.border_width, widget.vflags[corner_radius])
    else:
        pygame.draw.rect(screen, valpack.border_col, widget.get_rect(), valpack.border_width)
"""
Text
"""
def draw_text(label: Label, screen):
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color, label.bg)
    screen.blit(text_surface, label.get_pos())
def set_Bold(label: Label):
    label.font.set_bold(True)
    label.dirty_vflags.add(textpack)
    label.dirty_auto_flag.add(text_auto_resize)
def set_Italic(label: Label):
    label.font.set_italic(True)
    label.dirty_vflags.add(textpack)
    label.hide_itself()
    label.dirty_auto_flag.add(text_auto_resize)
def set_Underline(label: Label):
    label.font.set_underline(True)
    label.dirty_vflags.add(textpack)
    label.hide_itself()
    label.dirty_auto_flag.add(text_auto_resize)
def set_Strikethrough(label: Label):
    label.font.set_strikethrough(True)
    label.dirty_vflags.add(textpack)
    label.dirty_auto_flag.add(text_auto_resize)
def set_Antialias(label: Label):
    label.smooth = True
    label.dirty_vflags.add(textpack)
def set_have_Background(label: Label):
    if bg_color in label.vflags:
        label.bg = label.vflags[bg_color]
        label.dirty_vflags.add(textpack)
    else:
        raise ValueError('Background color is not found')
def text_resize(label: Label):
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    new_size = text_surface.get_size()
    label.Size_update(new_size)