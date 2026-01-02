import pygame
import timeit
from kernel import Margin, LayoutHelper
screen = pygame.Surface((800, 600))
w, h = screen.get_size()
pad_x, pad_y = 50, 50

# --- Manual Margin với đủ tính năng ---
manual_margin_cache = {}
anchors = ['TopLeft', 'TopCenter', 'TopRight',
           'CenterLeft', 'Center', 'CenterRight',
           'BottomLeft', 'BottomCenter', 'BottomRight']

def manual_margin_get_pos(obj_size, anchor):
    if anchor not in anchors:
        raise KeyError('Invalid anchor')
    key = (obj_size, anchor)
    if key in manual_margin_cache:
        return manual_margin_cache[key]
    w_o, h_o = obj_size
    left = pad_x
    center_x = (w - w_o) // 2
    right = w - w_o - pad_x
    top = pad_y
    center_y = (h - h_o) // 2
    bottom = h - h_o - pad_y
    if anchor == 'TopLeft': pos = (left, top)
    elif anchor == 'TopCenter': pos = (center_x, top)
    elif anchor == 'TopRight': pos = (right, top)
    elif anchor == 'CenterLeft': pos = (left, center_y)
    elif anchor == 'Center': pos = (center_x, center_y)
    elif anchor == 'CenterRight': pos = (right, center_y)
    elif anchor == 'BottomLeft': pos = (left, bottom)
    elif anchor == 'BottomCenter': pos = (center_x, bottom)
    elif anchor == 'BottomRight': pos = (right, bottom)
    manual_margin_cache[key] = pos
    return pos

# --- Manual LayoutHelper với đủ tính năng ---
def manual_layout_get_pos(obj_rect, next_size, direction, padding):
    ox, oy, ow, oh = obj_rect
    nw, nh = next_size
    px, py = padding
    if direction == 'Right':
        x = ox + ow + px
        y = oy + py
        if x + nw > w or y + nh > h or y < 0:
            raise ValueError('Out of screen')
    elif direction == 'Left':
        x = ox - px - nw
        y = oy + py
        if x < 0 or y + nh > h or y < 0:
            raise ValueError('Out of screen')
    elif direction == 'Down':
        x = ox + px
        y = oy + oh + py
        if y + nh > h or x + nw > w or x < 0:
            raise ValueError('Out of screen')
    elif direction == 'Up':
        x = ox + px
        y = oy - py - nh
        if y < 0 or x + nw > w or x < 0:
            raise ValueError('Out of screen')
    else:
        raise KeyError('Invalid direction')
    return x, y

# --- Benchmark ---

margin = Margin(screen, padding=(50, 50))
helper = LayoutHelper(screen)

def bench_kernel_margin():
    for _ in range(1000):
        margin.get_pos((100, 50), 'Center')
        margin.get_pos((200, 80), 'TopRight')
        margin.get_pos((60, 60), 'BottomLeft')

def bench_manual_margin():
    for _ in range(1000):
        manual_margin_get_pos((100, 50), 'Center')
        manual_margin_get_pos((200, 80), 'TopRight')
        manual_margin_get_pos((60, 60), 'BottomLeft')

def bench_kernel_layout():
    for _ in range(1000):
        helper.get_pos((100, 100, 50, 50), (30, 30), 'Right', (10, 0))
        helper.get_pos((100, 100, 50, 50), (40, 40), 'Down', (0, 5))
        helper.get_pos((100, 100, 50, 50), (20, 20), 'Left', (5, 5))

def bench_manual_layout():
    for _ in range(1000):
        manual_layout_get_pos((100, 100, 50, 50), (30, 30), 'Right', (10, 0))
        manual_layout_get_pos((100, 100, 50, 50), (40, 40), 'Down', (0, 5))
        manual_layout_get_pos((100, 100, 50, 50), (20, 20), 'Left', (5, 5))

count = 500
print("Benchmarking (fair comparison)...")
t_km = timeit.timeit(bench_kernel_margin, number=count) / count * 1000
t_mm = timeit.timeit(bench_manual_margin, number=count) / count * 1000
t_kl = timeit.timeit(bench_kernel_layout, number=count) / count * 1000
t_ml = timeit.timeit(bench_manual_layout, number=count) / count * 1000

print(f"Kernel Margin: {t_km:.3f} ms/call | Manual Margin: {t_mm:.3f} ms/call | Slowdown: {t_km/t_mm:.2f}x")
print(f"Kernel Layout: {t_kl:.3f} ms/call | Manual Layout: {t_ml:.3f} ms/call | Slowdown: {t_kl/t_ml:.2f}x")