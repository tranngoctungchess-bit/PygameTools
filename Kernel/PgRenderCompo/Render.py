import pygame

from Kernel.VFlags import *
from Kernel.UFlags import *
from Kernel.KernelWidget import Widget
from Kernel.PgRenderCompo.TextObj import Label

"""
Surface
"""


def get_rounded_surface(surface, radius):
    size = surface.get_size()
    target = pygame.Surface(size, pygame.SRCALPHA)
    target.fill((0, 0, 0, 0))
    pygame.draw.rect(target, (255, 255, 255, 255), (0, 0, size[0], size[1]), border_radius=radius)
    target.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return target
def fill_bg(widget: Widget, screen: pygame.Surface):
    bg = widget.vflags[bg_widget]
    radius = widget.vflags.get(corner_radius, 0)
    if isinstance(bg, tuple):
        pygame.draw.rect(screen, bg, (widget.rect.x, widget.rect.y, widget.rect.w, widget.rect.h), border_radius=radius)
    elif isinstance(bg, pygame.Surface):
        cache_key = f"_rounded_bg_cache_{widget.rect.w}_{widget.rect.h}_{radius}"
        rounded_bg = getattr(widget, cache_key, None)
        if rounded_bg is None:
            scaled_bg = pygame.transform.smoothscale(bg, (int(widget.rect.w), int(widget.rect.h)))
            if radius > 0:
                rounded_bg = get_rounded_surface(scaled_bg, radius)
            else:
                rounded_bg = scaled_bg
            setattr(widget, cache_key, rounded_bg)
        screen.blit(rounded_bg, (widget.rect.x, widget.rect.y))
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
    if bg_widget in label.vflags:
        label.bg = label.vflags[bg_widget]
        label.dirty_vflags.add(textpack)
    else:
        raise ValueError('Background color is not found')
def text_resize(label: Label):
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    new_size = text_surface.get_size()
    label.Size_update(new_size)