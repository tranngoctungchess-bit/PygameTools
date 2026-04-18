from pgtkb import (
    MainApplication, Label, FixedButton, text_Is_Antialias, Anchor,
    pressed_bg, ImagePack, Uplclick, Audio
)
import pygame

# --------------------------
# Âm thanh và ảnh
# --------------------------
baihat = Audio('hb.mp3')
baihat.set_volume(0.2)

mainapp = MainApplication((800, 600), caption="Chương trình sinh nhật")

natrue_start = ImagePack("startbg.png")
natrue_start.resize((800, 600))
flower = ImagePack("flower.png")
flower.resize((800, 600))

# --------------------------
# Giao diện ban đầu
# --------------------------
mainapp.screen.change_bg(natrue_start.get_image())
mainapp.screen.set_margin(border_percent=(30, 10))

hellolabel = Label(
    mainapp.screen,
    (0, 0, 0),
    24,
    "Màn hình chờ",
)
hellolabel.goto_margin(Anchor.topcenter)

startbutton = FixedButton(
    mainapp.screen,
    (200, 75),
    (255, 0, 100),
    pressbg=(255, 0, 255)
)
startbutton.goto_margin(Anchor.bottomcenter)
startbutton.set_margin()

startlabel = Label(
    startbutton,
    (0, 0, 0),
    24,
    "Start"
)
startlabel.goto_margin(Anchor.center)
def play_happybirthday():
    mainapp.screen.blank_newbg(flower.surface)
    baihat.set_volume(0.5)
    baihat.play()

startbutton.add_vflag((Uplclick, play_happybirthday))
event_manage = mainapp.event_manager
def handle_audio_keys():
    if event_manage.is_key_pressed(pygame.K_p):
        baihat.pause()
    elif event_manage.is_key_pressed(pygame.K_r):
        if baihat.is_paused:
            baihat.resume()
        elif baihat.is_playing():
            pass
    elif event_manage.is_key_pressed(pygame.K_a):
        baihat.play()
    elif event_manage.is_key_pressed(pygame.K_s):
        baihat.stop()
mainapp.add_action(handle_audio_keys)
mainapp.threadstart()