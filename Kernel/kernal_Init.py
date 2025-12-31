import pygame
init_state = False
def init():
    global init_state
    if not init_state:
        pygame.init()
        init_state = True

