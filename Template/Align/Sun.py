#CodeName: Sun
# cho một Obj, và tạo ra margin nhưng các obj sẽ sắp xếp xung quanh obj gốc
from kernel import LayoutHelper


class SunLayout:
    def __init__(self, screen, center_obj: tuple, padding=10):
        self.w_screen, self.h_screen = screen.get_size()
        self.w_obj, self.h_obj,self.width_obj,  self.length_obj = center_obj
        self.padding = padding
    def get_pos(self, slot, obj_size):
        pass