from Kernel.KernelWidget import Widget, ImmutableRect
from Kernel.ObjType import PosTuple


class GridLayout:
    def __init__(self, width_grid: int, height_grid: int, size: PosTuple, pos: PosTuple | None = None, padding=20):
        self.width_grid = width_grid
        self.height_grid = height_grid
        self.total_width, self.total_height = size
        self.pos = pos if pos is not None else (0, 0)
        self.padding = padding

        available_width = self.total_width - (2 * padding)
        available_height = self.total_height - (2 * padding)

        self.cell_width = available_width / width_grid
        self.cell_height = available_height / height_grid
        self.edge_cell = (self.cell_width, self.cell_height)

        self.cells = []

        cur_pos_x = self.pos[0] + padding

        for i in range(width_grid):
            row_cells = []
            cur_pos_y = self.pos[1] + padding

            for j in range(height_grid):
                cell = (cur_pos_x, cur_pos_y)
                row_cells.append(cell)
                cur_pos_y += self.cell_height

            self.cells.append(row_cells)
            cur_pos_x += self.cell_width

    def setpos(self, widget: Widget, cell_pos=tuple[int, int], center = True):
        xpos, ypos = cell_pos
        cell_x, cell_y = self.cells[xpos][ypos]
        w, h = widget.rect.w, widget.rect.h

        if center:
            final_x = cell_x + (self.cell_width - w) / 2
            final_y = cell_y + (self.cell_height - h) / 2
        else:
            final_x = cell_x
            final_y = cell_y
        if isinstance(widget.rect, ImmutableRect):
            widget.rect = ImmutableRect(final_x, final_y, w, h)
        else:
            widget.rect.x = final_x
            widget.rect.y = final_y

class HorizontalLayout(GridLayout):
    def __init__(self, length : int, size: PosTuple, pos : PosTuple, padding=20):
        super().__init__(length, 1, size, pos, padding)
class VerticalLayout(GridLayout):
    def __init__(self, length: int, size: PosTuple, pos: PosTuple, padding=20):
        super().__init__(1, length, size, pos, padding)
