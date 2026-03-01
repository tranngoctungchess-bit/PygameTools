import pygame


screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            print('resize')
        if event.type == pygame.QUIT:
            running = False
        screen.fill((0,0,0))
