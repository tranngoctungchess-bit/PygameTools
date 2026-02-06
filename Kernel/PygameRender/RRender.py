from Kernel.PygameRender.Render import *
from Kernel.Flags.RFlags import *
from Kernel.KernelWidget import Widget
from Kernel.PygameRender.Textobj import Label
def Remove_bg(widget: Widget, screen):
    if border in widget.vflags:
        set_border(widget, screen)
    else:
        widget.hide_itself()
def Remove_border(widget: Widget, screen):
    if bg_color in widget.vflags:
        fill_bg(widget, screen)
    else:
        widget.hide_itself()
def Remove_corner_radius(widget: Widget, screen):
    if border in widget.vflags:
        valpack = widget.vflags[border]
        pygame.draw.rect(screen, valpack.border_col, widget.get_rect(), valpack.border_width)
def Remove_textpack(label: Label, screen):
    if bg_color in label.vflags:
        fill_bg(label, screen)
    elif border in label.vflags:
        set_border(label, screen)
    else:
        widget.hide_itself()
def Remove_textBold(label: Label, screen):
    label.dirty_auto_flag.add(text_auto_resize)
    if bg_color in label.vflags:
        fill_bg(label, screen)
    else:
        label.hide_itself()
    label.font.set_bold(False)
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    screen.blit(text_surface, label.get_pos())
def Remove_textItalic(label: Label, screen):
    label.dirty_auto_flag.add(text_auto_resize)
    if bg_color in label.vflags:
        fill_bg(label, screen)
    else:
        label.hide_itself()
    label.font.set_italic(False)
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    screen.blit(text_surface, label.get_pos())
def Remove_textUnderline(label:Label, screen):
    label.dirty_auto_flag.add(text_auto_resize)
    if bg_color in label.vflags:
        fill_bg(label, screen)
    else:
        label.hide_itself()
    label.font.set_underline(False)
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    screen.blit(text_surface, label.get_pos())
def Remove_textStrikethrough(label:Label, screen):
    label.dirty_auto_flag.add(text_auto_resize)
    if bg_color in label.vflags:
        fill_bg(label, screen)
    else:
        label.hide_itself()
    label.font.set_strikethrough(False)
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    screen.blit(text_surface, label.get_pos())
def Remove_textAntialias(label : Label, screen):
    if bg_color in label.vflags:
        fill_bg(label, screen)
    else:
        label.hide_itself()
    label.smooth = False
    text_surface = label.font.render(label.textpack.Text, label.smooth, label.textpack.Color)
    screen.blit(text_surface, label.get_pos())
def Remove_textBg(label: Label, screen):
    label.hide_itself()
    font = label.font if hasattr(label, 'font') else \
        pygame.font.SysFont(label.textpack.Font, label.textpack.Size)

    font.set_bold(text_Is_Bold in label.uflags)
    font.set_italic(text_Is_Italic in label.uflags)
    font.set_underline(text_Is_Underline in label.uflags)
    font.set_strikethrough(text_Is_Strikethrough in label.uflags)

    text_surface = font.render(
        label.textpack.Text,
        text_Is_Antialias in label.uflags,
        label.textpack.Color
    )
    screen.blit(text_surface, label.get_pos())