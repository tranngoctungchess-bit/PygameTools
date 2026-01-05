#Kernel 1(build 0.02)
#Pre-alpha
from typing import Tuple, Union, Optional
import pygame
import kernal_Init

kernal_Init.init()
#####
#Margin
#####


class Margin:
    def __init__(self, screen ,percentage_padding: Optional[Tuple[float, float]] = (0,0), padding: Optional[Tuple[float, float]] = (0, 0)):
        self.width_screen, self.height_screen = screen.get_size()
        self.last_screen_size = (self.width_screen, self.height_screen)
        if 0 < percentage_padding[0] > 100 or 0 < percentage_padding[1] > 100:
            raise ValueError('Your padding must in range from 0 to 100')
        self.padding = padding
        self.percentage = percentage_padding
        if self.percentage:
            self.padding = (self.width_screen * self.percentage[0] / 100, self.height_screen * self.percentage[1] / 100)
        self.cache = {}
        self.cache_pos = {}
    def get_pos(self, obj: Tuple[Union[int, float], Union[int, float]], anchor: Optional[str]):
        if not anchor:
            if 'Anchor' in self.cache:
                anchor = self.cache['Anchor']

        w_o, h_o = obj
        if (w_o, h_o, anchor) in self.cache_pos:
            return self.cache_pos[(w_o, h_o, anchor)]

        w_s, h_s = self.width_screen, self.height_screen
        b_x, b_y = self.padding

        left = b_x
        center_x = (w_s - w_o) // 2
        right = w_s - w_o - b_x
        top = b_y
        center_y = (h_s - h_o) // 2
        bottom = h_s - h_o - b_y

        if anchor == 'TopLeft':
            pos = (left, top)
        elif anchor == 'TopCenter':
            pos = (center_x, top)
        elif anchor == 'TopRight':
            pos = (right, top)
        elif anchor == 'CenterLeft':
            pos = (left, center_y)
        elif anchor == 'Center':
            pos = (center_x, center_y)
        elif anchor == 'CenterRight':
            pos = (right, center_y)
        elif anchor == 'BottomLeft':
            pos = (left, bottom)
        elif anchor == 'BottomCenter':
            pos = (center_x, bottom)
        elif anchor == 'BottomRight':
            pos = (right, bottom)
        else:
            raise KeyError(f'Invalid anchor: {anchor}')

        self.cache_pos[(w_o, h_o, anchor)] = pos
        return pos
    def save_margin(self, anchor: str):
        if anchor in {
            'CenterRight': 0,
            'Center': 0,
            'CenterLeft' : 0,
            'TopCenter': 0,
            'TopLeft' : 0,
            'TopRight': 0,
            'BottomCenter': 0,
            'BottomLeft': 0,
            'BottomRight': 0
        }:
            self.cache['Anchor'] = anchor
        else:
            raise KeyError(f'Invalid anchor: {anchor}')
    def update_on_resize(self, screen):
        self.width_screen, self.height_screen = screen.get_size()
        if self.percentage:
            self.padding = (self.width_screen * self.percentage[0] / 100,
                            self.height_screen * self.percentage[1] / 100)
        self.last_screen_size = (self.width_screen, self.height_screen)
        self.cache_pos.clear()

    @property
    def content_rect(self):
        left, top = self.padding
        width = self.width_screen - 2 * self.padding[0]
        height = self.height_screen - 2 * self.padding[1]
        # Đảm bảo không âm
        width = max(0, width)
        height = max(0, height)
        return pygame.Rect(left, top, width, height)

######
#NEXT
######
class LayoutHelper:
    __slots__ = ('screen_w', 'screen_h')
    def __init__(self, screen):
        self.screen_w, self.screen_h = screen.get_size()
    def update_screen(self, screen):
        self.screen_w, self.screen_h = screen.get_size()

    def get_pos(self, obj_rect: tuple, next_obj_size, direction, padding=(0, 0)):
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h

        if direction == 'Right':
            x = ox + ow + px
            y = oy + py
            if x + nw > sw or y + nh > sh or y < 0:
                raise ValueError('Out of screen')
        elif direction == 'Left':
            x = ox - px - nw
            y = oy + py
            if x < 0 or y > sh - nh or y < 0:
                raise ValueError('Out of screen')
        elif direction == 'Down':
            x = ox + px
            y = oy + oh + py
            if y > sh - nh or x  > sw - nw or x < 0:
                raise ValueError('Out of screen')
        elif direction == 'Up':
            x = ox + px
            y = oy - py - nh
            if y < 0 or x > sw - nw or x < 0:
                raise ValueError('Out of screen')
        else:
            raise KeyError('Invalid direction')

        return x, y


class Grid:
    def __init__(self, rows, cols, screen, margin=(0, 0)):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.margin_x, self.margin_y = margin

        sw, sh = screen.get_size()
        usable_w = sw - 2 * self.margin_x
        usable_h = sh - 2 * self.margin_y

        self.cell_width = usable_w / cols
        self.cell_height = usable_h / rows

        if self.cell_width <= 0 or self.cell_height <= 0:
            raise ValueError("Grid cells would have non‑positive size (check margin).")

    def get_cell_rect(self, row, col, span_rows=1, span_cols=1):
        x = self.margin_x + col * self.cell_width
        y = self.margin_y + row * self.cell_height
        w = span_cols * self.cell_width
        h = span_rows * self.cell_height
        return pygame.Rect(x, y, w, h)

    def get_cell_center(self, row, col):
        rect = self.get_cell_rect(row, col)
        return rect.center

    def iter_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c, self.get_cell_rect(r, c)
