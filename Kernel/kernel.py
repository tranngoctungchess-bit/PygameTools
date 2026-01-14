#Kernel 1(build 0.02)
#Pre-alpha
from typing import Tuple, Union, Optional
import pygame
from Kernel import kernal_Init
import re
from Kernel import kernel_color

kernal_Init.init()
#####
#Margin
#####


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
    last_screen_size : tuple[int, int]
    Last updated screen size.
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
        return left, top, width, height

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
    def getpos_up(self, obj_rect: tuple, next_obj_size, padding=(0, 0)):
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy - py - nh
        if y < 0 or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_down(self, obj_rect: tuple, next_obj_size, padding=(0, 0)):
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy + oh + py
        if y > sh - nh or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_right(self, obj_rect: tuple, next_obj_size, padding=(0, 0)):
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + ow + px
        y = oy + py
        if x + nw > sw or y + nh > sh or y < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_left(self, obj_rect: tuple, next_obj_size, padding=(0, 0)):
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
        return x, y, w, h

    def get_cell_center(self, row, col):
        rect = self.get_cell_rect(row, col)
        return rect.x + rect.w, rect.y + rect.h

    def iter_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c, self.get_cell_rect(r, c)
class ColorTools:
    def name_to_hex(self, name: str) -> str:
        if hex_value := NAMES_TO_HEX.get(name.lower()):
            return hex_value
        raise ValueError(f'"{name}" is not defined as a named color in CSS3')
    def hex_to_rgb(self, hex_value: str):
        int_value = int(normalize_hex(hex_value)[1:], 16)
        return int_value >> 16, int_value >> 8 & 0xFF, int_value & 0xFF
    def name_to_rgb(self, name, spec='CSS3'):
        return hex_to_rgb(name_to_hex(name, spec=spec))
    def normolize_hex(self, hex_value : str):
        if (match := re.compile(r"^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$").match(hex_value)) is None:
            raise ValueError(f'"{hex_value}" is not a valid hexadecimal color value.')
        hex_digits = match.group(1)
        if len(hex_digits) == 3:
            hex_digits = "".join(2 * s for s in hex_digits)
        return f"#{hex_digits.lower()}"

    def hsl_to_rgb(self, hsl):
        h, s, l = [float(v) for v in hsl]

        if not (0.0 - FLOAT_ERROR <= s <= 1.0 + FLOAT_ERROR):
            raise ValueError("Saturation must be between 0 and 1.")
        if not (0.0 - FLOAT_ERROR <= l <= 1.0 + FLOAT_ERROR):
            raise ValueError("Lightness must be between 0 and 1.")

        if s == 0:
            return l, l, l

        if l < 0.5:
            v2 = l * (1.0 + s)
        else:
            v2 = (l + s) - (s * l)

        v1 = 2.0 * l - v2

        r = _hue2rgb(v1, v2, h + (1.0 / 3))
        g = _hue2rgb(v1, v2, h)
        b = _hue2rgb(v1, v2, h - (1.0 / 3))

        return r, g, b

    def rgb_to_hsl(self, rgb):
        r, g, b = [float(v) for v in rgb]

        for name, v in {'Red': r, 'Green': g, 'Blue': b}.items():
            if not (0 - FLOAT_ERROR <= v <= 1 + FLOAT_ERROR):
                raise ValueError("%s must be between 0 and 1. You provided %r."
                                 % (name, v))

        vmin = min(r, g, b)  ## Min. value of RGB
        vmax = max(r, g, b)  ## Max. value of RGB
        diff = vmax - vmin  ## Delta RGB value

        vsum = vmin + vmax

        l = vsum / 2

        if diff < FLOAT_ERROR:
            return 0.0, 0.0, l

        ##
        ## Chromatic data...
        ##

        ## Saturation
        if l < 0.5:
            s = diff / vsum
        else:
            s = diff / (2.0 - vsum)

        dr = (((vmax - r) / 6) + (diff / 2)) / diff
        dg = (((vmax - g) / 6) + (diff / 2)) / diff
        db = (((vmax - b) / 6) + (diff / 2)) / diff

        if r == vmax:
            h = db - dg
        elif g == vmax:
            h = (1.0 / 3) + dr - db
        elif b == vmax:
            h = (2.0 / 3) + dg - dr

        if h < 0: h += 1
        if h > 1: h -= 1

        return h, s, l


class GradientGenerator:
    def linear_gradient(self, color_start, color_end, steps):
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1)
            # Trộn màu
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            gradient.append((r, g, b))
        return gradient

    def multi_gradient(self, colors, steps):
        gradient = []
        segments = len(colors) - 1
        steps_per_segment = steps // segments

        for i in range(segments):
            segment_grad = self.linear_gradient(
                colors[i], colors[i + 1], steps_per_segment
            )
            gradient.extend(segment_grad)

        return gradientd
class Rect:
    def __init__(self, x: Union[int, float], y: Union[int, float], width: Union[int, float], height: Union[int, float]):
        """
        Rect:
        the base object for any widget class as bar, button coming soon in this tool
        x, y: the pos of rect
        width, height: the width and the height of this rect
        All the above values will be automatically converted to positive numbers.
        """
        self.x = abs(x)
        self.y = abs(y)
        self.width = abs(width)
        self.height = abs(height)
