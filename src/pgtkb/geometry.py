#v0.09
import math
#wrap some useful function from a math lib
sqrt = math.sqrt
atan2 = math.atan2
degrees = math.degrees
radians = math.radians
cos = math.cos
sin = math.sin
pi = math.pi
def to_vector(pos_x:float, pos_y:float):
    """change 2 pos to a vector"""
    return pos_y - pos_x
def magnitude(vec):
    """return the distance of two pos"""
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])
def vector_between(p1, p2):
    """return the vector between two pos"""
    return p2[0] - p1[0], p2[1] - p1[1]
def normalize(vec):
    """Return unit vector."""
    mag = magnitude(vec)
    if mag == 0:
        return 0.0, 0.0
    return vec[0] / mag, vec[1] / mag
def midpoint(p1, p2):
    """
    return the pos of the midpoint in the line
    """
    return (p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5
def point_on_circle(center, radius, angle_deg):
    """
    return position of the point in the circle
    """
    rad = math.radians(angle_deg)
    return (center[0] + radius * math.cos(rad),
            center[1] + radius * math.sin(rad))
def clamp_point(point, rect):
    """Clamp point to be inside rect (pygame.Rect or (x,y,w,h))."""
    x, y = point
    rx, ry, rw, rh = rect
    return (max(rx, min(x, rx + rw)),
            max(ry, min(y, ry + rh)))
def vector_to_angle(dx, dy):
    """
    Return angle in degrees (0° to 360°) of vector (dx, dy).
    0° points to the right (positive X), 90° points down (positive Y in pygame).
    """
    # math.atan2(dy, dx) returns radians, convert to degrees
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    # Normalize to 0–360
    return angle_deg % 360.0
# Rect utilities
def rect_intersection(rect1, rect2):
    """Return overlapping rect as pygame.Rect, or None if no intersection."""
    x1 = max(rect1[0], rect2[0])
    y1 = max(rect1[1], rect2[1])
    x2 = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
    y2 = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
    if x2 > x1 and y2 > y1:
        return x1, y1, x2 - x1, y2 - y1
    return None
def rect_union(rect1, rect2):
    """Return the smallest rect containing both rects."""
    x1 = min(rect1[0], rect2[0])
    y1 = min(rect1[1], rect2[1])
    x2 = max(rect1[0] + rect1[2], rect2[0] + rect2[2])
    y2 = max(rect1[1] + rect1[3], rect2[1] + rect2[3])
    return x1, y1, x2 - x1, y2 - y1

def rotate_point(point, center, angle_deg):
    """
    Rotate a point around a center by a given angle (degrees).
    Positive angle = counter‑clockwise (mathematical convention).
    """
    px, py = point
    cx, cy = center
    rad = radians(angle_deg)
    cos_a = cos(rad)
    sin_a = sin(rad)

    # Translate to origin
    dx = px - cx
    dy = py - cy

    # Rotate
    rx = dx * cos_a - dy * sin_a
    ry = dx * sin_a + dy * cos_a

    # Translate back
    return rx + cx, ry + cy
def pytagore(a, b):
    """Return sqrt(a² + b²) – Pythagorean distance for a right triangle."""
    return sqrt(a*a + b*b)
def law_of_cosines(a, b, angle_deg):
    """Return length of side c given sides a, b and included angle C in degrees."""
    rad = radians(angle_deg)
    return sqrt(a*a + b*b - 2*a*b*cos(rad))
def triangle_area(p1, p2, p3):
    """Area of triangle given three points (x, y)."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)
def point_line_distance(point, line_p1, line_p2):
    """Distance from point to line defined by two points."""
    x0, y0 = point
    x1, y1 = line_p1
    x2, y2 = line_p2
    numerator = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1))
    denominator = sqrt((x2-x1)**2 + (y2-y1)**2)
    if denominator == 0:
        return distance(point, line_p1)  # a line is a point
    return numerator / denominator
