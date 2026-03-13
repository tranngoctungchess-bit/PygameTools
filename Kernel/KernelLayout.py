from typing import Tuple, Union
import Kernel.KernelPosition
import pygame
import warnings
from KernelWidget import Widget, ImmutableRect, MutableRect
from Kernel.ObjType import MathVal2
class GridLayout:
    def __init__(self, width_grid: int, height_grid: int, size: MathVal2, pos: MathVal2| None=None):
        self.width_grid = width_grid
        self.height_grid = height_grid
        self.total_width, self.total_height = size
        self.pos = pos if pos is not None else (0, 0)

        self.cell_width = self.total_width / width_grid
        self.cell_height = self.total_height / height_grid
        self.edge_cell = (self.cell_width, self.cell_height)

        self.cells = []

        cur_pos_x = self.pos[0]

        for i in range(width_grid):
            row_cells = []
            cur_pos_y = self.pos[1]

            for j in range(height_grid):
                cell = (cur_pos_x, cur_pos_y)
                row_cells.append(cell)
                cur_pos_y += self.cell_height

            self.cells.append(row_cells)
            cur_pos_x += self.cell_width
    def setpos(self, widget: Widget, cell_pos= Tuple[int, int]):
        xpos, ypos = cell_pos
        x,y = self.cells[xpos][ypos]
        if isinstance(widget.rect, ImmutableRect):
            w, h = widget.rect.w, widget.rect.h
            widget.rect = ImmutableRect(x,y,w,h)
        else:
            widget.rect.x = x
            widget.rect.y = y


