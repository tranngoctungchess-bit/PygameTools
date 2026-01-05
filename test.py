import pygame
from Template.Align.MarginScreen import MarginScreen
from Template.Collision.VideoResize import VideoResize

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()
margin_screen = MarginScreen(800, 600, border_percent=(5, 10), resizeable=True)
vr = VideoResize(screen, [margin_screen])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if vr.check_update():
        vr.update()
        print(f"Screen resized to {screen.get_size()}")

    margin_screen.fill((30, 30, 30))
    margin_screen.update()
    clock.tick(60)

pygame.quit()