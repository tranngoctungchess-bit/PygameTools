import pygame
from Kernel import ObjType, Widget, corner_radius, border
from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender import Textobj
from Kernel.kernal_Init import should_fill
from Kernel.VFlags import bg_color
from Kernel.UFlags import *
pack = ObjType.TextPack((255,0,0), 'Arial', 20, 'Hello World')
rg = MainScreen((800,600))
obj = Textobj.Label(rg, pack, (100, 100))
obj.add_uflag(text_Is_Underline)
obj.add_uflag(text_Is_Antialias)
render = PygameRender(obj)
running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if obj.inrect(mouse):
                if text_Is_Underline in obj.uflags:
                    obj.remove_uflag(text_Is_Underline)
                else:
                    obj.add_uflag(text_Is_Underline)
    if should_fill():
        rg.fill((255, 255, 255))
    render.render()
    pygame.display.flip()