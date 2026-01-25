from typing import Tuple, Union
from collections import namedtuple
def createpairpack(Objname,valname1, valname2):
    return namedtuple(Objname, [valname1, valname2])
MathVal1 = Tuple[Union[int, float],Union[int, float],Union[int, float],Union[int, float]]
MathVal2 = Tuple[Union[int, float],Union[int, float]]
Border = createpairpack('Border', 'border_width', 'border_col')