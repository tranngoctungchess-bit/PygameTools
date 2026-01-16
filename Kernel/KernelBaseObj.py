import numpy as np
from typing import Tuple, Union, Optional, List
from dataclasses import dataclass
from collections import namedtuple
from Kernel.ObjType import MathVal2, MathVal1
"""
ImmutableRect and MutableRect:
the base object for any widget class as bar, button coming soon in this tool
x, y: the pos of rect
width, height: the width and the height of this rect
"""
ImmutableRect = namedtuple('Rect', ['x', 'y', 'w', 'h'])
@dataclass(slots = True)
class MutableRect:
    x:Union[int, float]
    y:Union[int,float]
    width:Union[int, float]
    height:Union[int,float]
class BP:
    """
    This is a tool class that helps convert the position of widgets to their actual position on the screen.
    """
    def __init__(self, dis: Optional[MathVal2] = None):
        self.dis_x, self.dis_y = dis
    def convert(self, x, y):
        return dis_x + x, dis_y + y
    def convert_a_lot(self, vals: List[MathVal2]):
        values = np.array(vals, dtype=float)
        return values + np.array([self.dis_x, self.dis_y])
class Object:
    """
    This is the base class of widget and all the Ui interface rectangle
    """
    pass