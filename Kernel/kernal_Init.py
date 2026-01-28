import pygame
init_state = False
_fill_mode = True

def set_fill_mode(mode=False):
    global _fill_mode
    _fill_mode = mode

def should_fill():
    return _fill_mode
def init():
    global init_state
    if not init_state:
        pygame.init()
        init_state = True
    set_fill_mode()

