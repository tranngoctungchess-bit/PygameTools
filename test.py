#import pygame
from Template.Align import MarginScreen
from Template.Align import Sun
import Kernel.geometry as kg
"""
pygame.init()
screen = MarginScreen.MarginScreen(800, 600, border_percent=(10, 10), resizeable=True)
Suntst = Sun.AroundLayoutPro(screen.display, center_obj=(400, 300, 100, 100), padding=10)
df = [(30, 30) for _ in range(12)]
positions = Suntst.circle(100, df, padding=12)
"""
running = True
print(kg.pytagore(3,4))
"""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.resize_screen_handle(event)

    screen.fill((0, 0, 0))
    for pos_x, pos_y in positions:
        pygame.draw.rect(screen.display, (255, 255, 255), (pos_x, pos_y, 30, 30))
    screen.update()

pygame.quit()
"""