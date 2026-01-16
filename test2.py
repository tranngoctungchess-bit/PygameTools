import pygame
from Template.Align import MarginScreen
from Kernel.KernelPosition import LayoutHelper
screen = MarginScreen.MarginScreen(800, 600, border_percent=(-10, -10), resizeable=True)
rect_size = pygame.Surface((100,100))
rect_size.fill((255, 0, 0))
pos = screen.get_pos((100,100), 'Center')
print(pos)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        screen.resize_screen_handle(event)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen.display, (255,0,0), (*pos, 100,100))
    screen.update()