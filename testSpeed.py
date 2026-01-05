import pygame
import time
from Template.Align.MarginScreen import MarginScreen

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Test 1: Creation and anchor_render
ms = MarginScreen(800, 600, border_percent=(5, 10))
test_surface = pygame.Surface((100, 50))

start = time.perf_counter()
for _ in range(1000):
    ms.anchor_render(test_surface, 'Center')
    ms.anchor_render(test_surface, 'TopRight')
    ms.anchor_render(test_surface, 'BottomLeft')
end = time.perf_counter()
print(f"1000 anchor_render calls: {(end-start)*1000:.2f} ms")
print(f"Per call: {(end-start)/3000*1000:.3f} ms")

# Test 2: Resize handling (if resizable)
ms_resizable = MarginScreen(800, 600, border_percent=(5, 10), resizeable=True)
event = pygame.event.Event(pygame.VIDEORESIZE, w=1024, h=768)
start = time.perf_counter()
for _ in range(500):
    ms_resizable.resize_screen_handle(event)
end = time.perf_counter()
print(f"500 resize events: {(end-start)*1000:.2f} ms")