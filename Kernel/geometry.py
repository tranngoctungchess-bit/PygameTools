#v0.04
import kernal_Init
import math
kernal_Init.init()
#Ko nên cho class nhiều vào đây, vì đây chỉ là tính toán
#code name: Geometry
sqrt = math.sqrt
atan2 = math.atan2
degrees = math.degrees
radians = math.radians
cos = math.cos
sin = math.sin
pi = math.pi
def to_vector(pos_x, pos_y):
    """change 2 pos to a vector"""
    return pos_y - pos_x
def magnitude(vec):
    """return the distance of two pos"""
    return math.sqrt(vec[0]**2 + vec[1]**2)
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
    return (p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5

def point_on_circle(center, radius, angle_deg):
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
    """Return smallest rect containing both rects."""
    x1 = min(rect1[0], rect2[0])
    y1 = min(rect1[1], rect2[1])
    x2 = max(rect1[0] + rect1[2], rect2[0] + rect2[2])
    y2 = max(rect1[1] + rect1[3], rect2[1] + rect2[3])
    return x1, y1, x2 - x1, y2 - y1


def rotate_point(point, center, angle_deg):
    """
    Rotate a point around a center by given angle (degrees).
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