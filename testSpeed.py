import pygame
import timeit
from kernel import Margin, LayoutHelper

# Khởi tạo pygame screen ảo (không hiển thị)
pygame.init()
screen = pygame.Surface((800, 600))

# 1. Benchmark Margin.get_pos()
margin = Margin(screen, padding=(50, 50))
def bench_margin():
    for _ in range(1000):
        margin.get_pos((100, 50), 'Center')
        margin.get_pos((200, 80), 'TopRight')
        margin.get_pos((60, 60), 'BottomLeft')

# 2. Benchmark LayoutHelper.get_pos()
helper = LayoutHelper(screen)
rect = pygame.Rect(100, 100, 50, 50)
def bench_layout():
    for _ in range(1000):
        helper.get_pos(rect, (30, 30), 'Right', (10, 0))
        helper.get_pos(rect, (40, 40), 'Down', (0, 5))
        helper.get_pos(rect, (20, 20), 'Left', (5, 5))

# 3. Benchmark thủ công (tính toán trực tiếp)
def bench_manual():
    w, h = 800, 600
    pad_x, pad_y = 50, 50
    for _ in range(1000):
        # Center
        x = (w - 100) // 2
        y = (h - 50) // 2
        # TopRight
        x = w - 200 - pad_x
        y = pad_y
        # BottomLeft
        x = pad_x
        y = h - 60 - pad_y

# Chạy benchmark
count = 1000
print("Benchmarking...")
t_margin = timeit.timeit(bench_margin, number=count) / count * 1000
t_layout = timeit.timeit(bench_layout, number=count) / count * 1000
t_manual = timeit.timeit(bench_manual, number=count) / count * 1000

print(f"Margin.get_pos(): {t_margin:.3f} ms per call")
print(f"LayoutHelper.get_pos(): {t_layout:.3f} ms per call")
print(f"Manual calculation: {t_manual:.3f} ms per call")
print(f"Slowdown Margin: {t_margin / t_manual:.1f}x")
print(f"Slowdown LayoutHelper: {t_layout / t_manual:.1f}x")