## SimpleDraw template

A minimal drawing wrapper for Pygame’s `pygame.draw` functions.  
It reduces boilerplate when drawing basic shapes and optionally returns the bounding rectangle.

### Basic usage
```python
from Template.Draw.SimpleDraw import SimpleDraw

draw = SimpleDraw(screen)
draw.rect((100, 100, 200, 80), col=(255, 0, 0))          # draws a red rectangle
draw.circle((400, 300), 50, col=(0, 255, 0))             # draws a green circle
draw.triangle((50, 50), (150, 50), (100, 150))           # draws a white triangle
```
## Flags
The rect, line, ellipse and triangle methods accept a flags parameter:

['Draw'] (default) – draw the shape.

['ReturnPos'] – return the shape’s bounding rectangle (x, y, width, height) without drawing.

['Draw', 'ReturnPos'] – draw and return the bounding rectangle.

## Included methods
rect(rect, col, flags)

circle(center, radius, col)

triangle(p1, p2, p3, col, flags)

line(start, end, col, flags)

ellipse(rect, col, flags)

## Note
This template is intentionally simple. For advanced drawing (gradients, textures, anti‑aliasing), use Pygame’s native functions or create a custom template.