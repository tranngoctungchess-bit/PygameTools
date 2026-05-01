import pygame
display_init_state = False
audio_init_state = False
font_init_state = False
joystick_init_state = False
_fill_mode = True

def set_fill_mode(mode=False):
    global _fill_mode
    _fill_mode = mode

def should_fill():
    global _fill_mode
    tfill = _fill_mode
    _fill_mode = False
    return tfill
def display_init():
    global display_init_state
    if not display_init_state:
        pygame.display.init()
        display_init_state = True
    set_fill_mode(_fill_mode)
    pygame.key.set_repeat(300, 50)
def audio_init():
    global audio_init_state
    if not audio_init_state:
        try:
            pygame.mixer.init()
            audio_init_state = True
        except pygame.error:
            print("Không tìm thấy thiết bị âm thanh!")
def joystick_init():
    global joystick_init_state
    if not joystick_init_state:
        pygame.joystick.init()
        joystick_init_state = True
def font_init():
    global font_init_state
    if not font_init_state:
        pygame.font.init()
        font_init_state = True