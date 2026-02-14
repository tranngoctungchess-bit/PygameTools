import pygame
from Kernel import ObjType
from Kernel.KernelWidget import PygameRender, MainScreen
from Kernel.PygameRender import Textobj
from Kernel.Flags.UFlags import *
from Kernel.Flags.VFlags import *
from Kernel.KernelRun import Thread
pack = ObjType.TextPack((255,0,0), 'Arial', 20, 'Hello World')
rg = MainScreen((800,600))
obj = Textobj.Label(rg, pack, (100, 100))
obj.add_uflag(text_Is_Underline, text_Is_Antialias)
render = PygameRender(obj)
def toogle(obj):
    if text_Is_Underline in obj.uflags:
        obj.remove_uflag(text_Is_Underline)
    else:
        obj.add_uflag(text_Is_Underline)
obj.add_vflag((Downlclick, toogle))
rg.addWidget(obj, 'obj')
def Logic():
    rg.fill((255,255,255))
    render.render()
game = Thread(rg, [Logic])
game.threadstart()