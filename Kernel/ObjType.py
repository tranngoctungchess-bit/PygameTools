from typing import Tuple, Union
from collections import namedtuple
MathVal1 = Tuple[Union[int, float],Union[int, float],Union[int, float],Union[int, float]]
MathVal2 = Tuple[Union[int, float],Union[int, float]]
Border = namedtuple('Border', ['border_width', 'border_col'])
TextPack = namedtuple('Text', ['Color', 'Font', 'Size', 'Text'])