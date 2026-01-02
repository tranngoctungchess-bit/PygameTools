#CodeName: Sun
from kernel import LayoutHelper
#This is the first template that have a pro version
"""
ArroundLayout – Basic surrounding layout (3x3 grid around a center object).
For advanced features (rotation, dynamic padding, auto‑spacing), see SunPro (available from v0.05).
"""
#(Đây là biến thể của Next, nó thêm hỗ trợ chéo) <- Bản chất của Sun
class AroundLayout:
    def __init__(self, screen, center_obj: tuple, padding=10):
        self.w_screen, self.h_screen = screen.get_size()
        self.x_obj, self.y_obj,self.width_obj,  self.length_obj = center_obj
        self.padding = padding
        self.child_obj_pos = {}
        self.Helper = LayoutHelper(screen)
        self.quicker_option = {'RightCenter' : 'Right', 'LeftCenter' : 'Left', 'TopCenter' : 'Up', 'BottomCenter' : 'Down'}
    def get_pos(self, slot, obj_size):
        try:
            cw, ch = obj_size
            if slot in self.quicker_option:
                self.child_obj_pos[slot] = obj_size
                return self.Helper.get_pos(
                    (self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                    obj_size, self.quicker_option[slot], (self.padding, self.padding)
                )
            self.child_obj_pos[slot] = obj_size
            offset_x = cw + self.padding
            # offset_y không cần vì 'Up'/'Down' đã tính đúng y

            if slot == 'TopLeft':
                base = self.Helper.get_pos((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, 'Up', (self.padding, self.padding))
                return base[0] - offset_x, base[1]
            elif slot == 'TopRight':
                base = self.Helper.get_pos((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, 'Up', (self.padding, self.padding))
                return base[0] + offset_x, base[1]
            elif slot == 'BottomLeft':
                base = self.Helper.get_pos((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, 'Down', (self.padding, self.padding))
                return base[0] - offset_x, base[1]
            elif slot == 'BottomRight':
                base = self.Helper.get_pos((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, 'Down', (self.padding, self.padding))
                return base[0] + offset_x, base[1]
            else:
                del self.child_obj_pos[slot]
                raise KeyError(f"Invalid slot: {slot}")
        except ValueError:
            raise ValueError('Cannot Put this Object because it is Out of Screen')
    def change_first_obj(self, new_obj, warning = True):
        self.x_obj, self.y_obj, self.width_obj, self.length_obj = new_obj
        failed_slots = []
        for slot in list(self.child_obj_pos.keys()):
            obj_size = self.child_obj_pos[slot]
            try:
                new_pos = self.get_pos(slot, obj_size)
                self.child_obj_pos[slot] = new_pos
            except ValueError:
                failed_slots.append(slot)
                del self.child_obj_pos[slot]
        if failed_slots and warning:
            import warnings
            warnings.warn(f"Slots {failed_slots} are out of screen after moving center object.")
class SunPro:
    def __init__(self):
        print('This template is being developed soon')
        print('please waiting for PygameTools v0.05')
    #Well, Tạo phiên bản nâng cao hơn cho sunlayout, nhưng nó sẽ ko thân thiện cho lắm, vậy nên, ai muốn đơn giản thì dùng Sunlayout Gốc

