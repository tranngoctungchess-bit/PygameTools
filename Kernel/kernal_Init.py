import pygame
init_ = False
def init():
    global init_
    if not init_:
        pygame.init()
        init_ = True

