## MissPoint template

Calculates missing geometric points for common shapes.  
Useful when you know part of a shape and need to compute the remaining vertices.

### Basic usage
```python
from Template.Draw.MissPoint import MissPoint

calc = MissPoint(screen)
p3 = calc.equilateral_triangle((100, 100), (200, 100))    # third point of an equilateral triangle
p4 = calc.parallelogram((0,0), (100,0), (50,50))          # fourth point of a parallelogram
corners = calc.rect_from_diagonal((10,10), (200,150))     # all four corners of a rectangle
```
## Methods
equilateral_triangle(p1, p2) – returns the third point of an equilateral triangle (left side of vector p1→p2).

parallelogram(p1, p2, p3) – returns the fourth point of a parallelogram (p1, p2, p3 in order).

rect_from_diagonal(p1, p3) – returns a tuple of four corners (p1, p2, p3, p4) of the rectangle.

circle_points(center, radius, n) – returns n evenly spaced points around a circle.

reflect_point(point, line_p1, line_p2) – reflects a point across a line.

## Note
This template only computes coordinates; you must draw the shapes yourself (e.g., with SimpleDraw or pygame.draw).
All coordinates are returned as (x, y) tuples.