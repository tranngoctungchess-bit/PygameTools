import pygame
from kernel import Next

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Tạo rect mẫu
obj_rect = pygame.Rect(100, 100, 50, 50)  # đối tượng gốc
next_rect = (0, 0, 30, 30)    # đối tượng muốn đặt cạnh

next_calc = Next(screen)

# Test các hướng
try:
    pos_right = next_calc.get_pos(obj_rect, next_rect, 'Left', (-10, 0))
    print('Right pos:', pos_right)
except ValueError as e:
    print(e)

try:
    pos_down = next_calc.get_pos(obj_rect, next_rect, 'Down', (0, 10))
    print('Down pos:', pos_down)
except ValueError as e:
    print(e)

# Test không đủ chỗ (ví dụ đặt lên trên nhưng obj_rect quá sát top)
obj_rect.top = 5
try:
    pos_up = next_calc.get_pos(obj_rect, next_rect, 'Up', (0, 10))
    print('Up pos:', pos_up)
except ValueError as e:
    print('Up error:', e)