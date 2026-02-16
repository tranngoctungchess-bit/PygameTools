from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender import ButtonObj
from Kernel.KernelRun import Thread, quitnow
screen = MainScreen((800, 600))
btn = ButtonObj.FixedButton(parent=screen,name="test_btn",rect=(100, 100, 200, 50),bg=(0,255,0),hoverbg=(255,255,0),pressbg=(255,125,0))
render = PygameRender(btn)
screen.addWidget(btn, "test_btn")
def Logic():
    screen.fill((255,255,255))
    render.render()
game = Thread(screen, [Logic], quitnow)
game.threadstart()