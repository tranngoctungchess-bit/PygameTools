from typing import Tuple, Union
import Kernel.KernelPosition
import pygame
import warnings
from Kernel.KernelPosition import LayoutHelper


class VerticalStack:
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
                    next_obj_pos = self.Manager.getpos_up(self.objects[-1], objSize, (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                else:
                    next_obj_pos = self.Manager.getpos_down(self.objects[-1], objSize, (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append((next_pos_x,next_pos_y,w_next,h_next))
                return next_obj_pos
            else:
                next_pos_x, next_pos_y = self.first_pos
                w_next, h_next = objSize
                self.objects.append((next_pos_x, next_pos_y, w_next, h_next))
        except ValueError:
            raise ValueError('Stack reached screen limit')
    def pop(self):
        return self.objects.pop()
    @property
    def total_length(self):
        if not self.objects:
            return 0
        if self.reverse:
            return abs(self.objects[0].bottom - self.objects[-1].top)
        else:
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
                    next_obj_pos = self.Manager.getpos_left(self.objects[-1], objSize, (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append(pygame.Rect(next_pos_x,next_pos_y,w_next,h_next))
                else:
                    next_obj_pos = self.Manager.getpos_right(self.objects[-1], objSize, (padding, 0.0))
                    next_pos_x, next_pos_y = next_obj_pos
                    w_next, h_next = objSize
                    self.objects.append((next_pos_x,next_pos_y,w_next,h_next))
                return next_obj_pos
            else:
                next_pos_x, next_pos_y = self.first_pos
                w_next, h_next = objSize
                self.objects.append((next_pos_x, next_pos_y, w_next, h_next))
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


class ProHorizontalStack:
    def __init__(self, screen, first_pos: Tuple[Union[int, float], Union[int, float]], reverse=False):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.first_pos = first_pos
        self.objects = []
        self.Manager = LayoutHelper(screen)
        self.reverse = reverse
        self.rows = []  # list of lists, each sublist is a row of rects

    def push(self, objSize, padding=0.0, wrap=True, max_shrink_attempts=5):
        if padding < 0:
            warnings.warn("padding is negative, items may overlap.", stacklevel=2)

        w, h = objSize
        if not self.objects:
            # First object ever
            rect = pygame.Rect(self.first_pos[0], self.first_pos[1], w, h)
            self.objects.append(rect)
            self.rows.append([rect])
            return rect.topleft

        # Try to place in the current row (last row in self.rows)
        current_row = self.rows[-1]
        last_in_row = current_row[-1]
        direction = 'Left' if self.reverse else 'Right'

        for shrink in range(max_shrink_attempts):
            current_padding = max(0, padding - shrink)  # reduce padding each attempt
            try:
                next_pos = self.Manager.get_pos(last_in_row, objSize, direction, (current_padding, 0))
                new_rect = pygame.Rect(next_pos[0], next_pos[1], w, h)
                # Check vertical fit (within screen)
                if new_rect.bottom > self.screen_rect.bottom:
                    raise ValueError("Bottom overflow")
                current_row.append(new_rect)
                self.objects.append(new_rect)
                return new_rect.topleft
            except ValueError:
                # Horizontal overflow or vertical overflow
                if shrink == max_shrink_attempts - 1:
                    # The last shrink attempt failed
                    if wrap:
                        # Start a new row below the first object of the first row
                        base_y = self.rows[0][0].bottom + current_padding
                        new_rect = pygame.Rect(self.first_pos[0], base_y, w, h)
                        if new_rect.bottom > self.screen_rect.bottom:
                            raise ValueError("Out of screen vertically, cannot wrap")
                        self.rows.append([new_rect])
                        self.objects.append(new_rect)
                        return new_rect.topleft
                    else:
                        raise ValueError("Out of screen and wrap is disabled")
                continue  # try smaller padding

    def pop(self):
        if not self.objects:
            raise IndexError("pop from empty stack")
        popped = self.objects.pop()
        # Remove from rows as well
        for row in self.rows:
            if popped in row:
                row.remove(popped)
                if not row:
                    self.rows.remove(row)
                break
        return popped

    @property
    def total_width(self):
        if not self.objects:
            return 0
        if self.reverse:
            return abs(self.objects[0].right - self.objects[-1].left)
        else:
            return abs(self.objects[-1].right - self.objects[0].left)

    @property
    def total_height(self):
        if not self.rows:
            return 0
        top = min(r.top for row in self.rows for r in row)
        bottom = max(r.bottom for row in self.rows for r in row)
        return bottom - top

    def clear(self):
        self.objects.clear()
        self.rows.clear()

    def __len__(self):
        return len(self.objects)


class ProVerticalStack:
    def __init__(self, screen, first_pos, reverse=False):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.first_pos = first_pos
        self.objects = []
        self.Manager = LayoutHelper(screen)
        self.reverse = reverse
        self.columns = []  # list of lists, each sublist is a column of rects

    def push(self, objSize, padding=0.0, wrap=True, max_shrink_attempts=5):
        if padding < 0:
            warnings.warn("padding is negative, items may overlap.", stacklevel=2)

        w, h = objSize
        if not self.objects:
            rect = pygame.Rect(self.first_pos[0], self.first_pos[1], w, h)
            self.objects.append(rect)
            self.columns.append([rect])
            return rect.topleft

        current_col = self.columns[-1]
        last_in_col = current_col[-1]
        direction = 'Up' if self.reverse else 'Down'

        for shrink in range(max_shrink_attempts):
            current_padding = max(0, padding - shrink)
            try:
                next_pos = self.Manager.get_pos(last_in_col, objSize, direction, (0, current_padding))
                new_rect = pygame.Rect(next_pos[0], next_pos[1], w, h)
                if new_rect.right > self.screen_rect.right:
                    raise ValueError("Right overflow")
                current_col.append(new_rect)
                self.objects.append(new_rect)
                return new_rect.topleft
            except ValueError:
                if shrink == max_shrink_attempts - 1:
                    if wrap:
                        # Start a new column to the right of the first column's first object
                        base_x = self.columns[0][0].right + current_padding
                        new_rect = pygame.Rect(base_x, self.first_pos[1], w, h)
                        if new_rect.right > self.screen_rect.right:
                            raise ValueError("Out of screen horizontally, cannot wrap")
                        self.columns.append([new_rect])
                        self.objects.append(new_rect)
                        return new_rect.topleft
                    else:
                        raise ValueError("Out of screen and wrap is disabled")
                continue

    def pop(self):
        if not self.objects:
            raise IndexError("pop from empty stack")
        popped = self.objects.pop()
        for col in self.columns:
            if popped in col:
                col.remove(popped)
                if not col:
                    self.columns.remove(col)
                break
        return popped

    @property
    def total_width(self):
        if not self.columns:
            return 0
        left = min(r.left for col in self.columns for r in col)
        right = max(r.right for col in self.columns for r in col)
        return right - left

    @property
    def total_height(self):
        if not self.objects:
            return 0
        if self.reverse:
            return abs(self.objects[0].bottom - self.objects[-1].top)
        else:
            return abs(self.objects[-1].bottom - self.objects[0].top)

    def clear(self):
        self.objects.clear()
        self.columns.clear()

    def __len__(self):
        return len(self.objects)