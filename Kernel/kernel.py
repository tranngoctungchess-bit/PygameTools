#Kernel 1 (Build 0.01)
#The first build of kernal
#Pre-alpha
from typing import Tuple, Union, Optional, Mapping
import pygame
import kernal_Init
kernal_Init.init()
class Margin:
    def __init__(self, screen ,percentage_padding: Optional[Tuple[float, float]] = None, padding: Optional[Tuple[float, float]] = (0, 0)):
        self.screen = screen
        self.width_screen = screen.get_width()
        self.height_screen = screen.get_height()
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
    def get_pos(self, obj: Tuple[Union[int, float], Union[int, float]], anchor: Optional[str]):
        if not anchor:
            if 'Anchor' in self.cache:
                anchor = self.cache[anchor]

        self.check_anchor_valid(anchor)
        return self.update_margin_map(obj)[anchor]

    def update_margin_map(self, obj: Tuple[float, float]):
        # Cập nhật lại kích thước màn hình mới nhất (phòng trường hợp resize)
        w_s, h_s = self.screen.get_size()
        w_o, h_o = obj
        b_x, b_y = self.padding

        # Tính toán các điểm tọa độ chính
        left = b_x
        center_x = (w_s - w_o) // 2
        right = w_s - w_o - b_x

        top = b_y
        center_y = (h_s - h_o) // 2
        bottom = h_s - h_o - b_y

        # Map các anchor với tọa độ tương ứng
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

        self.margin_map = positions
        return self.margin_map
    def save_margin(self, anchor: str):
        self.check_anchor_valid(anchor)
        self.cache['Anchor'] = anchor
    def check_anchor_valid(self, anchor):
        if anchor not in self.margin_map:
            raise KeyError('Your Margin is not valid')
class Next:
    def __init__(self,screen):
        self.w_screen = screen.get_width
        self.h_screen = screen.get_height
    def get_pos(self, obj_rect, next_obj_rect, next_dir, padding: Optional[Tuple[float, float]] = (0, 0)):
        if next_dir not in ['Right', 'Left', 'Up', 'Down']:
            raise KeyError('Your next position direction is not valid')
        if self.check_enough_size(obj_rect, next_obj_rect, next_dir, padding):
            pass
        pass

    def check_enough_size(self, obj_rect, next_obj_size, next_dir, padding):
        pass