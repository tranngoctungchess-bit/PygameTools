"""Module for managing screen positions, anchors, and layouts.

This module provides classes for handling object placement based on anchors (top-left, center, etc.),
margins/padding, and relative positioning between objects.
"""
from pgtkb.ObjType import PosTuple, RectTuple
class Anchor:
    """Constants for screen anchor positions."""
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
    """Manages margins and display positions for screen objects.

    This class handles padding calculation (absolute or percentage), anchor caching,
    and coordinate transformations based on screen size.

    Attributes:
        width_screen (int): Current screen width.
        Height_screen (int): Current screen height.
        Padding (tuple): Padding in pixels (x, y).
        Percentage (tuple, optional): Padding as a percentage of screen size (0-100).
        Cache (dict): Stores default anchor settings.
        Cache_pos (dict): Caches calculated positions for efficiency.
    """
    __slots__ = ('width_screen', 'height_screen', 'last_screen_size', 'padding', 'percentage', 'cache', 'cache_pos')
    def __init__(self, screen, percentage_padding: PosTuple | None = None, padding: PosTuple | None = (0, 0)):
        """Initializes the Margin manager.

        Args:
            screen: A surface or screen object with get_size() or get_width()/get_height().
            percentage_padding (PosTuple, optional): Padding as (x%, y%). Defaults to None.
            padding (PosTuple, optional): Fixed padding as (x, y) pixels. Defaults to (0, 0).
        """
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
        """Updates the fixed padding values.

        Args:
            new_padding (tuple): The new (x, y) padding in pixels.
        """
        self.padding = new_padding
    def get_pos(self, obj: PosTuple, anchor: str | None):
        """Calculates the (x, y) position of an object based on an anchor.

        Args:
            obj (PosTuple): The size of the object (width, height).
            anchor (str, optional): The anchor name (e.g., 'Center', 'TopLeft').
                If None, uses the cached default anchor.

        Returns:
            tuple: The calculated (x, y) coordinate.

        Raises:
            KeyError: If the anchor name is invalid.
        """
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
        """Saves a default anchor for future use in get_pos.

        Args:
            anchor (str): The anchor name to save (e.g., 'Center', 'BottomRight').

        Raises:
            KeyError: If the anchor name is invalid.
        """
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
        """Updates internal screen dimensions and recalculates padding on resize.

        Args:
            container: The new screen or surface container object.
        """
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
        """Calculates the available content area after subtracting padding.

        Returns:
            tuple: (left, top, width, height) of the content rectangle.
        """
        left, top = self.padding
        width = self.width_screen - 2 * self.padding[0]
        height = self.height_screen - 2 * self.padding[1]
        width = max(0, width)
        height = max(0, height)
        return left, top, width, height
class LayoutHelper:
    """Helper for positioning objects relative to other objects.

    Attributes:
        screen_w (int): Stored screen width.
        Screen_h (int): Stored screen height.
    """
    __slots__ = ('screen_w', 'screen_h')
    def __init__(self, screen):
        """Initializes the LayoutHelper.

        Args:
            screen: A surface or screen object with get_size().
        """
        self.screen_w, self.screen_h = screen.get_size()
    def update_screen(self, screen):
        """Updates the stored screen dimensions.

        Args:
            screen: A surface or screen object with get_size().
        """
        self.screen_w, self.screen_h = screen.get_size()

    def get_pos(self, obj_rect: RectTuple, next_obj_size: PosTuple, direction, padding=(0, 0)) -> tuple[float, float]:
        """Calculates the position of a new object relative to an existing one.

        Args:
            obj_rect (RectTuple): (x, y, w, h) of the existing object.
            next_obj_size (PosTuple): (w, h) of the object to be positioned.
            direction (str): 'Right', 'Left', 'Down', or 'Up'.
            padding (tuple, optional): (x, y) padding to apply. Defaults to (0, 0).

        Returns:
            tuple: The calculated (x, y) coordinate.

        Raises:
            KeyError: If the direction is invalid.
            ValueError: If the calculated position is outside the screen.
        """
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
        """Calculates the position above an existing object.

        Args:
            obj_rect (RectTuple): (x, y, w, h) of the existing object.
            next_obj_size (PosTuple): (w, h) of the next object.
            padding (tuple, optional): Padding to apply. Defaults to (0, 0).

        Returns:
            tuple: (x, y) coordinate.

        Raises:
            ValueError: If the position is outside the screen.
        """
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
        """Calculates the position below an existing object.

        Args:
            obj_rect (RectTuple): (x, y, w, h) of the existing object.
            next_obj_size (PosTuple): (w, h) of the next object.
            padding (tuple, optional): Padding to apply. Defaults to (0, 0).

        Returns:
            tuple: (x, y) coordinate.

        Raises:
            ValueError: If the position is outside the screen.
        """
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
        """Calculates the position to the right of an existing object.

        Args:
            obj_rect (RectTuple): (x, y, w, h) of the existing object.
            next_obj_size (PosTuple): (w, h) of the next object.
            padding (tuple, optional): Padding to apply. Defaults to (0, 0).

        Returns:
            tuple: (x, y) coordinate.

        Raises:
            ValueError: If the position is outside the screen.
        """
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
        """Calculates the position to the left of an existing object.

        Args:
            obj_rect (RectTuple): (x, y, w, h) of the existing object.
            next_obj_size (PosTuple): (w, h) of the next object.
            padding (tuple, optional): Padding to apply. Defaults to (0, 0).

        Returns:
            tuple: (x, y) coordinate.

        Raises:
            ValueError: If the position is outside the screen.
        """
        ox, oy, ow, oh = obj_rect
        nw, nh = next_obj_size
        px, py = padding
        sw, sh = self.screen_w, self.screen_h
        x = ox - px - nw
        y = oy + py
        if x < 0 or y > sh - nh or y < 0:
            raise ValueError('Out of screen')
        return x, y