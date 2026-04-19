from typing import Tuple, Optional
from pgtkb.ObjType import PosTuple, RectTuple
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
    def __init__(self, screen, percentage_padding: PosTuple | None = None, padding: PosTuple | None = (0, 0)):
        if hasattr(screen, 'get_size'):
            self.width_screen, self.height_screen = screen.get_size()
        else:
            self.width_screen, self.height_screen = screen.get_width(), screen.get_height()

        self.percentage = percentage_padding

        if self.percentage:
            self.padding = (self.width_screen * self.percentage[0] / 100,
                            self.height_screen * self.percentage[1] / 100)
        else:
            self.padding = padding if padding is not None else (0, 0)

        self.cache = {}
        self.cache_pos = {}
    def update_padding(self, new_padding):
        self.padding = new_padding
    def get_pos(self, obj: PosTuple, anchor: str | None):
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
        match anchor:
            case 'TopLeft':
                pos = (left, top)
            case 'TopCenter':
                pos = (center_x, top)
            case 'TopRight':
                pos = (right, top)
            case 'CenterLeft':
                pos = (left, center_y)
            case 'Center':
                pos = (center_x, center_y)
            case 'CenterRight':
                pos = (right, center_y)
            case 'BottomLeft':
                pos = (left, bottom)
            case 'BottomCenter':
                pos = (center_x, bottom)
            case 'BottomRight':
                pos = (right, bottom)
            case _:  # Trường hợp mặc định (tương đương else)
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

    def update_on_resize(self, container):
        if hasattr(container, 'get_size'):
            self.width_screen, self.height_screen = container.get_size()
        elif hasattr(container, 'get_width'):
            self.width_screen, self.height_screen = container.get_width(), container.get_height()

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

    def get_pos(self, obj_rect: RectTuple, next_obj_size: PosTuple, direction, padding=(0, 0)) -> tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h

        match direction:
            case 'Right':
                x, y = ox + ow + px, oy + py
            case 'Left':
                x, y = ox - px - nw, oy + py
            case 'Down':
                x, y = ox + px, oy + oh + py
            case 'Up':
                x, y = ox + px, oy - py - nh
            case _:
                raise KeyError('Invalid direction')

        if x < 0 or y < 0 or (x + nw > sw) or (y + nh > sh):
            raise ValueError('Out of screen')

        return x, y
    def getpos_up(self, obj_rect: RectTuple, next_obj_size: PosTuple, padding=(0, 0))-> tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy - py - nh
        if y < 0 or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_down(self, obj_rect: RectTuple, next_obj_size: PosTuple, padding=(0, 0))-> tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + px
        y = oy + oh + py
        if y > sh - nh or x > sw - nw or x < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_right(self, obj_rect: RectTuple, next_obj_size: PosTuple, padding=(0, 0))-> tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox + ow + px
        y = oy + py
        if x + nw > sw or y + nh > sh or y < 0:
            raise ValueError('Out of screen')
        return x, y
    def getpos_left(self, obj_rect: RectTuple, next_obj_size: PosTuple, padding=(0, 0))-> tuple[float, float]:
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox - px - nw
        y = oy + py
        if x < 0 or y > sh - nh or y < 0:
            raise ValueError('Out of screen')
        return x, y