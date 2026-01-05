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

## AroundLayoutPro template

Extended version of `AroundLayout` (Sun) with circular arrangement, auto‑positioning relative to screen edges, and alignment correction.

### Features
- **Circle layout** – place objects evenly around a circle with adjustable padding.
- **Screen‑edge positioning** – automatically place the center object at N equally spaced points around the screen.
- **Fix alignment** – adjust object positions to avoid overlaps and screen overflow by reducing padding iteratively.
- **Rotation** – rotate the whole layout by a given step.

### Basic usage
```python
from Template.Align.AroundLayoutPro import AroundLayoutPro

pro = AroundLayoutPro(screen, center_obj=(400,300,100,100), padding=15)
positions = pro.circle(radius=150, defined_obj=[(60,40), (70,50)], angle=0)
rotated = pro.rotate(count=1)
aligned = pro.fix_align(objects, center_obj, layout_type='circle', layout_params={'radius':150})
screen_layout = pro.get_to_screen(distance_to_screen=30, count=8, index=2)
```
## Notes
fix_align requires layout_type and layout_params to recalculate positions when padding is reduced.

circle padding is tangential (arc‑wise) spacing.

get_to_screen uses count to divide the screen perimeter into equal segments.

For simple surrounding layouts, use the basic AroundLayout (Sun).