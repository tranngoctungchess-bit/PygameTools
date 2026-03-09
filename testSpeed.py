from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender.Textobj import Label
from Kernel.PygameRender import ButtonObj
from Kernel.KernelRun import Thread, quitnow
from Kernel.Flags.UFlags import *
from Kernel.KernelPosition import Anchor
screen = MainScreen((800, 600), bg=(255,255,255))
WelcomeText = Label(screen, (0,0,0), 'Arial', 24, 'WelcomeToDemo','wlcTxt', (text_Is_Antialias, text_Is_Bold))
WelcomeText.set_render_engine(PygameRender)
WelcomeText.set_margin(Anchor.topcenter, percentage_padding=(50,0))
PlayButton = ButtonObj.FixedButton(screen, 'playbutton', (200,100), (255,0,255),pressbg=(0,255,123))
PlayButton.set_render_engine(PygameRender)
PlayButton.set_margin(Anchor.center)
PlayText = Label(PlayButton, (0,0,0), 'Arial', 20, 'PLAY', 'Playtxt', (text_Is_Bold,))
PlayText.set_render_engine(PygameRender)
PlayText.set_margin(Anchor.center)
game = Thread(screen, [WelcomeText.render, PlayButton.render, PlayText.render], quitnow)
game.threadstart()