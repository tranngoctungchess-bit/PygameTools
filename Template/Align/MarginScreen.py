from typing import Optional, Tuple
import pygame
from Kernel import KernelPosition
class MarginScreen:
    """
        Initialize a MarginScreen with built-in margin/padding and optional resize support.

        MarginScreen provides a convenient wrapper around pygame display with integrated margin management.
        It uses a 9-point anchor system to automatically position objects on screen with consistent padding.

        Parameters
        ----------
        width : int
            Initial width of the display window in pixels.
        height : int
            Initial height of the display window in pixels.
        border_percent : tuple[float, float] or None
            Padding as percentage of screen dimensions (x_percent, y_percent).
            Values should be in range 0-100. Applied symmetrically (left/right and top/bottom).
            Example: (5, 10) applies 5% horizontal and 10% vertical padding.
        resizeable : int, optional
            Flag to enable window resizing. Use 1 or True for resizable, 0 or False for fixed size.
            Default is 0 (fixed size).

        Attributes
        ----------
        display : pygame.Surface
            The pygame display surface object.
        margin_manager : KernelPosition.Margin
            Internal Margin manager for handling padding calculations and positioning.
        width : int
            Current display width in pixels.
        height : int
            Current display height in pixels.
        resizeable : int or bool
            Whether the window is resizable.
        flags : int
            Pygame display flags (pygame.RESIZABLE if resizable, 0 otherwise).

        Supported Anchors
        -----------------
        TopLeft, TopCenter, TopRight
        CenterLeft, Center, CenterRight
        BottomLeft, BottomCenter, BottomRight

        Examples
        --------
        >>> # Create a fixed-size screen with 5% horizontal and 10% vertical padding
        >>> screen = MarginScreen(800, 600, border_percent=(5, 10), resizeable=False)
        >>> screen.anchor_render(button_img, 'Center')
        >>> screen.update()

        >>> # Create a resizable screen
        >>> screen = MarginScreen(800, 600, border_percent=(5, 10), resizeable=True)
        >>> # In your event loop:
        >>> if event.type == pygame.VIDEORESIZE:
        ...     screen.resize_screen_handle(event)

        Notes
        -----
        - Call resize_screen_handle(event) in your event loop to handle window resize events
        - Call update() to refresh the display after rendering
        - Padding is calculated as a percentage of the current screen dimensions
        - When resizing, margins are automatically recalculated based on new screen size
    """
    def __init__(self, width: int, height: int, border_percent: Optional[Tuple[float, float]], resizeable = 0):
        self.flags = pygame.RESIZABLE if resizeable else 0
        self.display = pygame.display.set_mode((width, height), flags=self.flags)
        self.margin_manager = KernelPosition.Margin(self.display, padding=border_percent)
        self.width = width
        self.height = height
        self.resizeable = resizeable
    def get_pos(self, obj_size: Optional[Tuple[float, float]], anchor: str):
        return self.margin_manager.get_pos(obj_size, anchor)
    def fill(self, color):
        self.display.fill(color)
    def anchor_render(self, surface: pygame.Surface, anchor: str):
        pos = self.get_pos(surface.get_size(), anchor)
        self.display.blit(surface, pos)
    def update(self):
        pygame.display.flip()
    def resize_screen_handle(self, event):
        if event.type == pygame.VIDEORESIZE and self.resizeable:
            self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.margin_manager.update_on_resize(self.display)
            self.width, self.height = event.w, event.h