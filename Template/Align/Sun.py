import warnings
from Kernel.ObjType import MathVal2, MathVal1
from Kernel.KernelPosition import LayoutHelper
import math
"""
ArroundLayout – Basic surrounding layout (3x3 grid around a center object).
For advanced features (rotation, dynamic padding, auto‑spacing), see SunPro (available from v0.05).
"""
class AroundLayout:
    def __init__(self, screen, center_obj: MathVal1, padding=10):
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
            if slot == 'TopLeft':
                base = self.Helper.getpos_up((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, (self.padding, self.padding))
                return base[0] - offset_x, base[1]
            elif slot == 'TopRight':
                base = self.Helper.getpos_up((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, (self.padding, self.padding))
                return base[0] + offset_x, base[1]
            elif slot == 'BottomLeft':
                base = self.Helper.getpos_down((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, (self.padding, self.padding))
                return base[0] - offset_x, base[1]
            elif slot == 'BottomRight':
                base = self.Helper.getpos_down((self.x_obj, self.y_obj, self.width_obj, self.length_obj),
                                           obj_size, (self.padding, self.padding))
                return base[0] + offset_x, base[1]
            else:
                del self.child_obj_pos[slot]
                raise KeyError(f"Invalid slot: {slot}")
        except ValueError:
            raise ValueError('Cannot Put this Object because it is Out of Screen')
    def change_first_obj(self, new_obj: MathVal1, warning = True):
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


class AroundLayoutPro:
    def __init__(self, screen, center_obj: MathVal1, padding=10):
        self.screen = screen
        self.center = center_obj
        self.padding = padding
        self.start_angle = 0

    def circle(self, radius, defined_obj: list, angle='auto', padding=0, warn = False):
        """
        defined_obj: list of (width, height).
        angle: starting angle in degrees, or 'auto' for even distribution.
        padding: minimum space between objects (tangential).
        Returns: list of (x, y) positions for each object.
        """
        if radius > min(screen_size)/2 and warn:
            warnings.warn("Your obj can be out of screen")
        cx = self.center[0] + self.center[2] // 2
        cy = self.center[1] + self.center[3] // 2
        n = len(defined_obj)

        if n == 0:
            return []
        if angle == 'auto':
            delta_angle = 2 * math.pi / n
            start_angle = 0
        else:
            start_angle = math.radians(float(angle))
            max_size = max(max(w, h) for w, h in defined_obj)
            delta_angle = (max_size + padding) / max(radius, 1)

            if n * delta_angle > 2 * math.pi:
                raise ValueError("Objects too large or too many for the given radius and padding.")

        positions = []
        for i in range(n):
            theta = start_angle + i * delta_angle
            x = cx + radius * math.cos(theta) - defined_obj[i][0] // 2
            y = cy + radius * math.sin(theta) - defined_obj[i][1] // 2
            positions.append((x, y))

        return positions

    def rotate(self, count=1):
        """Rotate the layout by `count` steps (each step = 360°/n)."""
        self.start_angle += 360 * count
        self.start_angle %= 360

    def get_to_screen(self, distance_to_screen: float, count=4, index=0):
        """
        Place the center object at one of `count` equally spaced positions around the screen.
        Index: 0 to count‑1 (0 = right, then counter‑clockwise).
        """
        sw, sh = self.screen.get_size()
        cw, ch = self.center[2], self.center[3]

        radius = min(sw - cw, sh - ch) / 2 - distance_to_screen
        if radius < 0:
            radius = 0

        angle_step = 2 * math.pi / count
        angle = angle_step * index

        center_x = sw // 2
        center_y = sh // 2

        obj_x = center_x + radius * math.cos(angle)
        obj_y = center_y + radius * math.sin(angle)

        x = obj_x - cw // 2
        y = obj_y - ch // 2

        x = max(distance_to_screen, min(x, sw - cw - distance_to_screen))
        y = max(distance_to_screen, min(y, sh - ch - distance_to_screen))

        new_center = (int(x), int(y), cw, ch)
        return AroundLayout(self.screen, new_center, self.padding)

    def fix_align(self, objects: list, center_obj: MathVal1, layout_type='circle', layout_params=None):
        if layout_params is None:
            layout_params = {}

        sw, sh = self.screen.get_size()
        center_rect = pygame.Rect(center_obj) if isinstance(center_obj, tuple) else center_obj

        def recalc_positions(padding):
            if layout_type == 'circle':
                radius = layout_params.get('radius', 100)
                angle = layout_params.get('start_angle', 0)
                return self.circle(radius, [r.size for r in objects], angle)
            elif layout_type == 'sun':
                sun = AroundLayout(self.screen, center_rect, padding)
                positions = []
                for i, rect in enumerate(objects):
                    slot = layout_params.get('slots', ['TopCenter'] * len(objects))[i]
                    positions.append(sun.get_pos(slot, rect.size))
                return positions
            else:
                raise ValueError(f"Unsupported layout_type: {layout_type}")

        padding = self.padding
        for attempt in range(10):
            new_positions = recalc_positions(padding)
            rects = [pygame.Rect(pos, obj.size) for pos, obj in zip(new_positions, objects)]

            all_ok = True
            for rect in rects:
                if rect.colliderect(center_rect):
                    all_ok = False
                    break
                for other in rects:
                    if rect is other:
                        continue
                    if rect.colliderect(other):
                        all_ok = False
                        break
                if rect.left < 0 or rect.right > sw or rect.top < 0 or rect.bottom > sh:
                    all_ok = False
                    break

            if all_ok:
                return rects

            padding = max(0, padding - 5)

        raise ValueError("Alignment failed after reducing padding to zero.")