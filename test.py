import pygame
from Kernel import ObjType, ImagePack
from Kernel.KernelWidget import PygameRender, MainScreen
rg = MainScreen((800,600))
haha = ImagePack('haha.png')
haha.scale_resize(0.25)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    rg.fill((255,255,255))
    rg.blit(haha.get_image(), (100,100))
    pygame.display.flip()