#Kernel 1(build 0.02)
#Pre-alpha
from typing import Tuple, Union, Optional, Mapping
import pygame
import kernal_Init
kernal_Init.init()



#####
#Margin
#####


class Margin:
    def __init__(self, screen ,percentage_padding: Optional[Tuple[float, float]] = None, padding: Optional[Tuple[float, float]] = (0, 0)):
        self.screen = screen
        self.width_screen = screen.get_width()
        self.height_screen = screen.get_height()
        self.last_screen_size = (self.width_screen, self.height_screen)
        if 0 < padding[0] > 100 or 0 < padding[1] > 100:
            raise ValueError('Your padding must in range from 0 to 100')
        self.padding = padding
        self.percentage = percentage_padding
        if self.percentage:
            self.padding = (self.width_screen * self.percentage[0] / 100, self.height_screen * self.percentage[1] / 100)
        self.margin_map = {
            'CenterRight': 0,
            'Center': 0,
            'CenterLeft' : 0,
            'TopCenter': 0,
            'TopLeft' : 0,
            'TopRight': 0,
            'BottomCenter': 0,
            'BottomLeft': 0,
            'BottomRight': 0
        }
        self.cache = {}
        self.cache_pos = {}
    def get_pos(self, obj: Tuple[Union[int, float], Union[int, float]], anchor: Optional[str]):
        if not anchor:
            if 'Anchor' in self.cache:
                anchor = self.cache['Anchor']
        self.check_anchor_valid(anchor)

        w_o, h_o = obj
        key = (w_o, h_o, anchor)

        w_s, h_s = self.screen.get_size()
        if (w_s, h_s) != self.last_screen_size:
            self.update_on_resize(self.screen)

        if key in self.cache_pos:
            return self.cache_pos[key]

        pos = self._calculate_pos(obj, anchor)
        self.cache_pos[key] = pos
        return pos
    def _calculate_pos(self, obj, anchor):
        w_s, h_s = self.width_screen, self.height_screen
        w_o, h_o = obj
        b_x, b_y = self.padding

        left = b_x
        center_x = (w_s - w_o) // 2
        right = w_s - w_o - b_x

        top = b_y
        center_y = (h_s - h_o) // 2
        bottom = h_s - h_o - b_y

        positions = {
            'TopLeft': (left, top),
            'TopCenter': (center_x, top),
            'TopRight': (right, top),
            'CenterLeft': (left, center_y),
            'Center': (center_x, center_y),
            'CenterRight': (right, center_y),
            'BottomLeft': (left, bottom),
            'BottomCenter': (center_x, bottom),
            'BottomRight': (right, bottom)
        }
        return positions[anchor]
    def save_margin(self, anchor: str):
        self.check_anchor_valid(anchor)
        self.cache['Anchor'] = anchor
    def check_anchor_valid(self, anchor):
        if anchor not in self.margin_map:
            raise KeyError('Your Margin is not valid')

    def update_on_resize(self, screen):
        self.screen = screen
        self.width_screen = screen.get_width()
        self.height_screen = screen.get_height()
        if self.percentage:
            self.padding = (self.width_screen * self.percentage[0] / 100,
                            self.height_screen * self.percentage[1] / 100)
        self.last_screen_size = (self.width_screen, self.height_screen)
        self.cache_pos.clear()

    @property
    def content_rect(self):
        left = self.padding[0]
        top = self.padding[1]
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
    def __init__(self,screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
    def get_pos(self, obj_rect: Union[Tuple[Union[int, float], Union[int, float], Union[int, float], Union[int, float]],
                pygame.Rect],
                next_obj_size: Tuple[Union[int, float], Union[int, float]],
                next_dir: str, padding: Optional[Tuple[float, float]] = (0, 0)
                ):
        if isinstance(obj_rect, tuple):
            obj_rect = pygame.Rect(*obj_rect)
        if next_dir not in ['Right', 'Left', 'Up', 'Down']:
            raise KeyError('Your next position direction is not valid')
        if self.check_enough_size(obj_rect, next_obj_size, next_dir, padding):
            pad_x, pad_y = padding
            w_next_obj = next_obj_size[0]
            h_next_obj = next_obj_size[1]
            if next_dir == 'Up':
                x = obj_rect.x + pad_x
                y = obj_rect.top - pad_y - h_next_obj
            elif next_dir == 'Down':
                x = obj_rect.x + pad_x
                y = obj_rect.bottom + pad_y
            elif next_dir == 'Right':
                x = obj_rect.right + pad_x
                y = obj_rect.y + pad_y
            else:  # Left
                x = obj_rect.left - pad_x - w_next_obj
                y = obj_rect.y + pad_y

            return x, y
        else:
            raise ValueError('Your object is out of screen')

    def check_enough_size(self, obj_rect, next_obj, next_dir, padding):
        w_next_obj, h_next_obj = next_obj[0], next_obj[1]
        pad_x, pad_y = padding
        w_screen, h_screen = self.screen.get_rect().size

        if next_dir == 'Up':
            return (obj_rect.y - pad_y - h_next_obj >= 0 and
                    0 <= obj_rect.x + pad_x <= w_screen - w_next_obj)
        elif next_dir == 'Down':
            return (obj_rect.y + pad_y + h_next_obj <= h_screen and
                    0 <= obj_rect.x + pad_x <= w_screen - w_next_obj)
        elif next_dir == 'Right':
            return (obj_rect.x + pad_x + w_next_obj <= w_screen and
                    0 <= obj_rect.y + pad_y <= h_screen - h_next_obj)
        else:  # Left
            return (obj_rect.x - pad_x - w_next_obj >= 0 and
                    0 <= obj_rect.y + pad_y <= h_screen - h_next_obj)