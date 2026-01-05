import pygame
import time
from Template.Layout.StackLayout import VerticalStack

pygame.init()
screen = pygame.display.set_mode((800, 600))

stack = VerticalStack(screen, first_pos=(100, 100), reverse=False)
obj_sizes = [(80, 40), (90, 50), (70, 60)] * 3  # 9 objects

# Test push nhiều lần (mỗi lần tạo stack mới để không bị out‑of‑screen)
start = time.perf_counter()
for _ in range(500):
    temp_stack = VerticalStack(screen, first_pos=(100, 100))
    for sz in obj_sizes:
        temp_stack.push(sz, padding=10)
end = time.perf_counter()

total_pushes = 500 * len(obj_sizes)
print(f"500 stacks * {len(obj_sizes)} pushes = {total_pushes} total pushes")
print(f"Total time: {(end-start)*1000:.2f} ms")
print(f"Per push: {(end-start)/total_pushes*1000:.3f} ms")