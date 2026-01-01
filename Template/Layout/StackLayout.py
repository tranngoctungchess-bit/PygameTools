#CodeName : Verista
from typing import Tuple, Union

import kernel
import pygame
import warnings
from kernel import LayoutHelper


class VerticalStack:
    def __init__(self, screen, first_pos: Tuple[Union[int, float], Union[int, float]], reverse = False):
        self.first_pos = first_pos
        self.objects = []
        self.Manager = LayoutHelper(screen)
        self.reverse = reverse
    def push(self, objSize: Tuple[Union[int, float], Union[int, float]], padding = 0.0):
        #stack này ko cho chỉnh padding của height và ko cho padding là số âm
        if padding < 0:
            warnings.warn("padding is negative, items may overlap.", stacklevel=2)
        try:
            if self.objects:
                if self.reverse:
                    next_obj_pos = self.Manager.get_pos(self.objects[-1], objSize, 'Up', (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                else:
                    next_obj_pos = self.Manager.get_pos(self.objects[-1], objSize, 'Down', (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                return next_obj_pos
            else:
                next_pos_x, next_pos_y = self.first_pos
                w_next, h_next = objSize
                self.objects.append(pygame.Rect(next_pos_x, next_pos_y, w_next, h_next))
        except ValueError:
            raise ValueError('Stack reached screen limit')
    def pop(self):
        return self.objects.pop()
    @property
    def total_length(self):
        if not self.objects:
            return 0
        if self.reverse:
            # Chiều từ dưới lên trên
            return abs(self.objects[0].bottom - self.objects[-1].top)
        else:
            # Chiều từ trên xuống dưới
            return abs(self.objects[-1].bottom - self.objects[0].top)

    def clear(self):
        self.objects.clear()
    def __len__(self):
        return len(self.objects)
class HorizontalStack:
    def __init__(self, screen, first_pos: Tuple[Union[int, float], Union[int, float]], reverse = False):
        self.first_pos = first_pos
        self.objects = []
        self.Manager = LayoutHelper(screen)
        self.reverse = reverse
    def push(self, objSize: Tuple[Union[int, float], Union[int, float]], padding = 0.0):
        if padding < 0:
            warnings.warn("padding is negative, items may overlap.", stacklevel=2)
        try:
            if self.objects:
                if self.reverse:
                    next_obj_pos = self.Manager.get_pos(self.objects[-1], objSize, 'Left', (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                else:
                    next_obj_pos = self.Manager.get_pos(self.objects[-1], objSize, 'Right', (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                return next_obj_pos
            else:
                next_pos_x, next_pos_y = self.first_pos
                w_next, h_next = objSize
                self.objects.append(pygame.Rect(next_pos_x, next_pos_y, w_next, h_next))
        except ValueError:
            raise ValueError('Stack reached screen limit')
    def pop(self):
        return self.objects.pop()
    @property
    def total_length(self):
        if not self.objects:
            return 0
        if self.reverse:
            return abs(self.objects[0].right - self.objects[-1].left)
        else:
            return abs(self.objects[-1].right - self.objects[0].left)
    def clear(self):
        self.objects.clear()
    def __len__(self):
        return len(self.objects)