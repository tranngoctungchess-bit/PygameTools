from typing import Tuple
from Kernel import Widget, valid_background, Downrclick, PygameRender
from Kernel.Flags.VFlags import hover_bg, bg_widget, pressed_bg
from Kernel.ObjType import MathVal1
class FixedButton(Widget):
    def __init__(self, parent,name,  rect: MathVal1, bg=None, hoverbg=None, pressbg=None):
        super().__init__(parent, rect,bg=bg, name=name)
        self.is_hovered = False
        self.lock_hover = False
        if valid_background(bg):
            self.add_vflag((bg_widget, bg))
        self.bg = bg
        if valid_background(hoverbg):
            self.add_vflag((hover_bg, hoverbg))
        if valid_background(pressbg):
            self.add_vflag((pressed_bg, pressbg))
    def set_hoverbg(self, hoverbg):
        if valid_background(hoverbg):
            self.add_vflag((hover_bg, hoverbg))
    def set_pressbg(self, pressbg):
        if valid_background(pressbg):
            self.add_vflag((press_bg, pressbg))
    def set_disablebg(self, disablebg):
        if valid_background(disablebg):
            self.add_vflag((disable_bg, disablebg))