import pygame

from Kernel.PgRenderCompo.ButtonObj import FixedButton
from Kernel.UFlags import *
from Kernel.KernelWidget import Widget, MainScreen
from Kernel.ObjType import RectTuple, PosTuple, TextPack, Border
from Kernel.VFlags import *
import re
def trashfunc(*args, **kwargs):
    pass
re_search = re.search
re_findall = re.findall
re_sub = re.sub
re_split = re.split
re_match = re.match
re_compile = re.compile
re_escape = re.escape
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
URL_PATTERN = re.compile(r'https?://\S+')
HASHTAG_PATTERN = re.compile(r'#\w+')
MENTION_PATTERN = re.compile(r'@\w+')
def extract_emails(text):
    return EMAIL_PATTERN.findall(text)
def extract_urls(text):
    return URL_PATTERN.findall(text)
def extract_hashtags(text):
    return HASHTAG_PATTERN.findall(text)
def safe_substitute(text, pattern, replacement):
    """Safe regex substitution với escape"""
    return re_sub(re_escape(pattern), replacement, text)
#wrap
SysFont = pygame.font.SysFont
Font = pygame.font.Font
class Label(Widget):
    __slots__ = ('font', 'textpack', 'smooth', 'bg')
    def __init__(self, parent: Widget  | MainScreen, color,
                 size, text,
                  Uflags: set | tuple = (), pos : PosTuple=(0, 0), font ="timesnewroman", name: None | str = None):
        self.textpack = TextPack(color, font, size, text)
        self.font = pygame.font.SysFont(self.textpack.Font, self.textpack.Size)
        text_surface = self.font.render(self.textpack.Text, False, self.textpack.Color)
        pygameRect = text_surface.get_rect()
        x,y = pos
        tuple_rect = (x,y,pygameRect.w, pygameRect.h)
        super().__init__(parent, rect=tuple_rect,name=name, can_change=True)
        self.add_vflag((textpack, TextPack(color, font, size, text)))
        if isinstance(Uflags, set):
            self.uflags = Uflags
            self.dirty_uflags = Uflags
        else:
            for flag in Uflags:
                self.add_uflag(flag)
        self.smooth = text_Is_Antialias in self.uflags
        self.bg = None
    def smooth_update(self):
        self.smooth = text_Is_Antialias in self.uflags
    def Rect_update(self, rect: RectTuple):
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.rect.w = rect[2]
        self.rect.h = rect[3]
    def Size_update(self, size: PosTuple):
        self.rect.w = size[0]
        self.rect.h = size[1]
    def change_text(self, new_text: str):
        self.hide_itself()
        self.textpack.Text = new_text
        new_w, new_h = self.font.size(self.textpack.Text)
        self.Size_update((new_w, new_h))
        self.dirty_vflags.add(textpack)
class LineEdit(FixedButton):
    def __init__(self, parent,  text_size, width_line_edit ,pos: PosTuple=(0,0), bg=(255,255,255),
                 text_color=(0,0,0), border_radius=4, border_width=1, border_color = (0,0,0),
                 text_font="timesnewroman", text_uflags=None, pad_x=8, pad_y=4, name: str | None = None):
        text_uflags = {text_Is_Antialias} if not text_uflags else text_uflags
        text_pos = (pad_x + border_width, pad_y + border_width)
        temp_font = pygame.font.SysFont(text_font, text_size)
        height_line_edit = temp_font.get_height() + pad_y * 2 + border_width * 2
        rect = (pos[0], pos[1], width_line_edit, height_line_edit)
        super().__init__(parent, rect, bg, name=name)
        self.label = Label(self, text_color, text_size, "", text_uflags, text_pos, font=text_font)
        self.add_vflag((border, Border(border_width, border_color)))
        self.add_vflag((corner_radius, border_radius))
        self.text = self.label.textpack.Text
        self.display_text = self.text
        self.fully = False
        self.display_start = 0
        self.pad_x = pad_x
        self.pad_y = pad_y

    def _update_display_offset(self):
        b_width = self.vflags[border].border_width
        max_width = self.rect.w - self.pad_x * 2 - b_width * 2
        while True:
            current_w = self.label.font.size(self.text[self.display_start:])[0]
            if current_w <= max_width or self.display_start >= len(self.text):
                break
            self.display_start += 1
            self.fully = True
        while self.display_start > 0:
            test_start = self.display_start - 1
            test_w = self.label.font.size(self.text[test_start:])[0]
            if test_w <= max_width:
                self.display_start = test_start
            else:
                break
        if self.display_start == 0:
            self.fully = False
        self.label.change_text(self.text[self.display_start:])
    def process_addchar(self, char: str):
        self.text += char
        self._update_display_offset()
    def process_backspace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
            self._update_display_offset()

    def dispatch_hover(self, mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        return super().dispatch_hover(mouse_pos)

    def dispatch_release(self, mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return super().dispatch_release(mouse_pos)
    def clear_text(self):
        self.text = ""
        self._update_display_offset()