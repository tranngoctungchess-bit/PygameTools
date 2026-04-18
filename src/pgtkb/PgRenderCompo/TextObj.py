import pygame

from pgtkb.PgRenderCompo.ButtonObj import FixedButton
from pgtkb.UFlags import *
from pgtkb.KernelWidget import Widget, MainScreen
from pgtkb.ObjType import RectTuple, PosTuple, TextPack, Border
from pgtkb.VFlags import *
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
                  Uflags: set | tuple = (text_Is_Antialias,), pos : PosTuple=(0, 0), font ="timesnewroman", name: None | str = None):
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
    __slots__ = ("label", "text", "display_text", "fully", "display_start", "pad_x", "pad_y", "cursor", "cursor_idx",
                        "cursor_timer", "blink_speed")
    def __init__(self, parent,  text_size, width_line_edit ,pos: PosTuple=(0,0), bg=(255,255,255),
                 text_color=(0,0,0), border_radius=4, border_width=1, border_color = (0,0,0),
                 text_font="timesnewroman", text_uflags=None, pad_x=8, pad_y=4, name: str | None = None,
                 cursor_color=(0,0,0)):
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
        cursor_rect = (pad_x- 2, pad_y, 1, self.label.font.size(self.label.textpack.Text)[1])
        self.cursor = Cursor(self, cursor_color, cursor_rect)
        self.cursor_idx = 0
        self.cursor_timer = 0
        self.blink_speed = 0.5
        self.is_key_insert = False
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
        if self.is_key_insert and self.cursor_idx < len(self.text):
            self.text = self.text[:self.cursor_idx] + char + self.text[self.cursor_idx + 1:]
        else:
            self.text = self.text[:self.cursor_idx] + char + self.text[self.cursor_idx:]

        self.cursor_idx += 1
        self._update_display_offset()
        self._update_cursor_width()
        self.change_cursor_pos(0)

    def process_backspace(self):
        if self.cursor_idx > 0:
            self.text = self.text[:self.cursor_idx - 1] + self.text[self.cursor_idx:]
            self.cursor_idx -= 1
            self._update_display_offset()
            self.change_cursor_pos(0)

    def dispatch_hover(self, mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        return super().dispatch_hover(mouse_pos)

    def dispatch_release(self, mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return super().dispatch_release(mouse_pos)
    def clear_text(self):
        self.text = ""
        self._update_display_offset()
    def change_cursor_pos(self, addition_idx):
        self.cursor.hide_itself()
        # max(0, ...) ensures it doesn't go back past the beginning of the string,
        # min(..., len) ensures it doesn't go past the end of the string.
        self.cursor_idx = max(0, min(len(self.text), self.cursor_idx + addition_idx))
        self._update_cursor_width()
        text_segment = self.text[self.display_start: self.cursor_idx]
        width_to_cursor = self.label.font.size(text_segment)[0]
        new_x = self.label.rect.x + width_to_cursor
        #update widget cursor pos
        self.cursor.change_loc(new_x)
        self.label.rerender()
        self._reset_cursor_blink()

    def update(self, dt):
        if not self.focused:
            if self.cursor.visible:
                self.cursor.make_invisible()
            return
        self.cursor_timer += dt
        if self.cursor_timer >= self.blink_speed:
            self.cursor.visible = not self.cursor.visible
            if self.cursor.visible:
                self.cursor.make_visible()
            else:
                self.cursor.make_invisible()
            self.label.rerender()
            self.cursor_timer = 0
    def _reset_cursor_blink(self):
        self.cursor_timer = 0
        self.cursor.visible = True
        self.cursor.make_visible()
    def on_enter(self):
        pass

    def on_insert(self):
        self.cursor.make_invisible()
        self.is_key_insert = not self.is_key_insert
        self._update_cursor_width()
        self._reset_cursor_blink()

    def _update_cursor_width(self):
        if self.is_key_insert:
            if self.cursor_idx >= len(self.text):
                self.cursor.rect.w = 8
            else:
                char_to_overwrite = self.text[self.cursor_idx]
                char_w = self.label.font.size(char_to_overwrite)[0]
                self.cursor.rect.w = max(char_w, 8)
        else:
            self.cursor.rect.w = 1
        self.cursor.rerender()
class Cursor(Widget):
    def __init__(self,parent: FixedButton, color, rect):
        self.color = color
        super().__init__(parent, rect,can_change=True)
        self.visible = False
    def make_visible(self):
        self.add_vflag((bg_widget, self.color))
        self.visible = True
    def make_invisible(self):
        self.visible = False
        self.hide_itself()
    def change_loc(self, new_loc: int | float | PosTuple, pos_type: str = 'x'):
        if not isinstance(new_loc, int) and not isinstance(new_loc, float):
            self.change_pos(new_loc)
        else:
            if pos_type == 'x':
                self.rect.x = new_loc
            elif pos_type == 'y':
                self.rect.y = new_loc
            else:
                raise ValueError("invalid pos type")