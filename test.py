from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender import ButtonObj
from Kernel.KernelRun import Thread, quitnow
from Kernel.Flags.VFlags import Downlclick, Uplclick
from Kernel.KernelPosition import Anchor
screen = MainScreen((800, 600), bg=(255,255,255))
screen.set_caption("the test")
btn = ButtonObj.FixedButton(parent=screen,name="test_btn",rect=(200, 50),bg=(0,255,0),pressbg=(255,125,0))
btn.set_margin(Anchor.center)
def hello():
    print("Hello")
def goodbye():
    print("Goodbye")
btn.add_vflag((Downlclick, hello), (Uplclick, goodbye))
render = PygameRender(btn)
screen.addWidget(btn, "test_btn")
game = Thread(screen, [render.render], quitnow)
game.threadstart()