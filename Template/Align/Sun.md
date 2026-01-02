# SunLayout Template

Places objects in a 3×3 grid around a central object.

## When to use
- Quick placement of buttons, icons, or panels around a main element.
- HUD layouts where elements surround a character/vehicle.
- Menu systems with a central control.

## Basic usage
```python
from SunLayout import SunLayout

layout = SunLayout(screen, center_obj=(x, y, width, height), padding=20)
pos = layout.get_pos('TopCenter', (60, 40))

```
## Supported Slots
TopCenter, BottomCenter, LeftCenter, RightCenter

TopLeft, TopRight, BottomLeft, BottomRight

## Note
Uses LayoutHelper kernel for positioning and boundary checks.
If a slot went off‑screen, ValueError is raised.
Call change_first_obj(new_rect) to move the entire layout.

