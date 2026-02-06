#Kernel 1(build 0.09)
#Pre-alpha
from collections import namedtuple
from typing import Tuple, Union, Optional, List
import pygame
from Kernel.KernalInit import init
from Kernel.ObjType import MathVal2, MathVal1
init()
#####
#Margin
#####
class Anchor:
     topleft = 'TopLeft'
     topcenter = 'TopCenter'
     topright = 'TopRight'
     centerleft = 'CenterLeft'
     center = 'Center'
     centerright = 'CenterRight'
     bottomleft = 'BottomLeft'
     bottomcenter = 'BottomCenter'
     bottomright = 'BottomRight'
class Margin:
    """
    Manages margins and the display position of objects on the screen.
    This class supports:
    - Calculating padding based on percentage or absolute value.
    - Storing default anchors to position objects.
    - Caching calculated position results to improve performance.
    - Updating when the screen size changes.
    - Returning the content area (content_rect) after padding is subtracted.
    Attributes
    width_screen : int
    Current screen width.
    height_screen : int
    Current screen height.
    padding : tuple[float, float]
    Padding by pixels (x, y).
    percentage : tuple[float, float]
    Padding by percentage (0–100).
    cache : dict
    Stores default anchors.
    cache_pos : dict
    Caches the calculated position for the object.
    Methods:
    get_pos(obj, anchor):
    Calculates the (x, y) position of the object based on the anchor.
    Save_margin(anchor):
    Saves the default anchor for later use.
    Update_on_resize(screen):
    Updates screen size and padding when resizing.
    content_rect:
    Returns the remaining content area after subtracting padding.
    """
    __slots__ = ('width_screen', 'height_screen', 'last_screen_size', 'padding', 'percentage', 'cache', 'cache_pos')
    def __init__(self, screen ,percentage_padding: Optional[MathVal2] = None, padding: Optional[MathVal2] = (0, 0)):
        self.width_screen, self.height_screen = screen.get_size()
        self.percentage = percentage_padding
        if self.percentage:
            if 0 < percentage_padding[0] > 100 or 0 < percentage_padding[1] > 100:
                raise ValueError('Your padding must in range from 0 to 100')
            self.padding = (self.width_screen * self.percentage[0] / 100, self.height_screen * self.percentage[1] / 100)
        self.padding = padding
        self.cache = {}
        self.cache_pos = {}
    def get_pos(self, obj: MathVal2, anchor: Optional[str]):
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
        self.cache_pos.clear()

    @property
    def content_rect(self):
        left, top = self.padding
        width = self.width_screen - 2 * self.padding[0]
        height = self.height_screen - 2 * self.padding[1]
        width = max(0, width)
        height = max(0, height)
        return left, top, width, height

######
#NEXT
######
class LayoutHelper:
    """
    Docstring for LayoutHelper:
    A utility class to calculate the position of a new object relative to an existing object's rectangle.
    It supports positioning in four directions: 'Right', 'Left', 'Down', and 'Up', with optional padding.
    Attributes:
    screen_w : int
        Current screen width.
    screen_h : int
        Current screen height.
    Methods:
    update_screen(screen):
        Updates the stored screen dimensions.
    Get_pos(obj_rect, next_obj_size, direction, padding=(0, 0)):
        Calculates the position for the new object based on the specified direction and padding.
    Getpos_up(obj_rect, next_obj_size, padding=(0, 0)):
        Calculates the position above the existing object.
    Getpos_down(obj_rect, next_obj_size, padding=(0, 0)):
        Calculates the position below the existing object.
    Getpos_right(obj_rect, next_obj_size, padding=(0, 0)):
        Calculates the position to the right of the existing object.
    Getpos_left(obj_rect, next_obj_size, padding=(0, 0)):
        Calculates the position to the left of the existing object.
    """
    __slots__ = ('screen_w', 'screen_h')
    def __init__(self, screen):
        self.screen_w, self.screen_h = screen.get_size()
    def update_screen(self, screen):
        self.screen_w, self.screen_h = screen.get_size()

    def get_pos(self, obj_rect: MathVal1, next_obj_size: MathVal2, direction, padding=(0, 0)) -> Tuple[float, float]:
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
    def getpos_up(self, obj_rect: MathVal1, next_obj_size: MathVal2, padding=(0, 0))-> Tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy - py - nh
        if y < 0 or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_down(self, obj_rect: MathVal1, next_obj_size: MathVal2, padding=(0, 0))-> Tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy + oh + py
        if y > sh - nh or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_right(self, obj_rect: MathVal1, next_obj_size: MathVal2, padding=(0, 0))-> Tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + ow + px
        y = oy + py
        if x + nw > sw or y + nh > sh or y < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_left(self, obj_rect: MathVal1, next_obj_size: MathVal2, padding=(0, 0))-> Tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox - px - nw
        y = oy + py
        if x < 0 or y > sh - nh or y < 0:
            raise ValueError('Out of screen')
        return x, y
class Grid:
    """
    Docstring for Grid
    A utility class to divide the screen into a grid layout and calculate cell positions.
    Attributes:
    rows : int
        Number of rows in the grid.
    cols : int
        Number of columns in the grid.
    screen : pygame.Surface
        The screen surface to base the grid on.
    margin_x : int
        Horizontal margin around the grid.
    margin_y : int
        Vertical margin around the grid.
    cell_width : float
        Width of each grid cell.
    cell_height : float
        Height of each grid cell.
    Methods:
    get_cell_rect(row, col, span_rows=1, span_cols=1):
        Returns the rectangle (x, y, w, h) of the specified cell, optionally spanning multiple rows/columns.
    Get_cell_center(row, col):
        Returns the center (x, y) position of the specified cell.
    Iter_cells():
        Yields (row, col, rect) for each cell in the grid.
    """
    __slots__ = ('rows', 'cols', 'screen', 'margin_x', 'margin_y', 'cell_width', 'cell_height')
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

    def get_cell_rect(self, row, col, span_rows=1, span_cols=1) -> Tuple[float, float, float, float]:
        x = self.margin_x + col * self.cell_width
        y = self.margin_y + row * self.cell_height
        w = span_cols * self.cell_width
        h = span_rows * self.cell_height
        return x, y, w, h

    def get_cell_center(self, row, col) -> Tuple[float, float]:
        rect = self.get_cell_rect(row, col)
        return rect.x + rect.w, rect.y + rect.h

    def iter_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c, self.get_cell_rect(r, c)

