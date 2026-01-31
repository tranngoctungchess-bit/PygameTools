import pygame
from Kernel import ObjType, Widget, corner_radius, border
from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender import Textobj
from Kernel.kernal_Init import should_fill
from Kernel.VFlags import bg_color
pack = ObjType.TextPack((255,0,0), 'Arial', 20, 'Hello World')
rg = MainScreen((800,600))
obj = Textobj.Label(rg, pack, rect=(100,100,100,100))
render = PygameRender(obj)
running = True
rtext = True
w = [obj]
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if obj.inrect(mouse):
                if rtext:
                    w.pop()
                    new = Widget(rg, (100, 100, 100, 100))
                    new.set_flags(vflags=((bg_color, (255, 0, 0)),))
                    w.append(new)
                    render = PygameRender(w[0])
                    rtext = False
                else:
                    w.pop()
                    new = Textobj.Label(rg, pack, rect=(100, 100, 100, 100))
                    w.append(new)
                    render = PygameRender(w[0])
                    rtext = True
    if should_fill():
        rg.fill((255, 255, 255))
    render.render()
    pygame.display.flip()