import math
#wrap some useful function from a math lib
sqrt = math.sqrt
atan2 = math.atan2
degrees = math.degrees
radians = math.radians
cos = math.cos
sin = math.sin
pi = math.pi
def to_vector(p1, p2):
    """Return the vector from point p1 to point p2."""
    return p2[0] - p1[0], p2[1] - p1[1]

def distance(p1, p2):
    """Return the Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def lerp(a, b, t):
    """Linear interpolation between two numbers or points."""
    if isinstance(a, (list, tuple)):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return a + (b - a) * t

def dot_product(v1, v2):
    """Return the dot product of two vectors."""
    return v1[0] * v2[0] + v1[1] * v2[1]

def is_point_in_circle(point, center, radius):
    """Check if a point is inside a circle."""
    return distance(point, center) <= radius

def reflect_vector(vec, normal):
    """Reflect a vector across a surface normal (bouncing logic)."""
    n = normalize(normal)
    dot = dot_product(vec, n)
    return (vec[0] - 2 * dot * n[0], vec[1] - 2 * dot * n[1])

def get_bounding_box(points):
    """Return (x, y, w, h) that encloses all given points."""
    if not points: return None
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return (min_x, min_y, max_x - min_x, max_y - min_y)

def magnitude(vec):
    """return the distance of two pos"""
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def vector_between(p1, p2):
    """return the vector between two pos"""
    return to_vector(p1, p2)
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

def normalize_angle(angle):
    """Normalize angle to [0, 360)."""
    return angle % 360.0

def angle_difference(target, current):
    """Return the shortest difference between two angles in degrees."""
    diff = (target - current + 180) % 360 - 180
    return diff

def line_intersection(p1, p2, p3, p4):
    """
    Find the intersection point of two line segments (p1-p2) and (p3-p4).
    Returns (x, y) if they intersect, else None.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if denom == 0:  # Parallel or coincident
        return None

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    if 0 <= ua <= 1 and 0 <= ub <= 1:
        return x1 + ua * (x2 - x1), y1 + ua * (y2 - y1)
    return None

def is_point_in_triangle(p, a, b, c):
    """Check if point p is inside triangle abc using barycentric coordinates."""
    px, py = p
    ax, ay = a
    bx, by = b
    cx, cy = c

    v0 = (cx - ax, cy - ay)
    v1 = (bx - ax, by - ay)
    v2 = (px - ax, py - ay)

    dot00 = dot_product(v0, v0)
    dot01 = dot_product(v0, v1)
    dot02 = dot_product(v0, v2)
    dot11 = dot_product(v1, v1)
    dot12 = dot_product(v1, v2)

    denom = (dot00 * dot11 - dot01 * dot01)
    if denom == 0: return False # Degenerate triangle
    
    inv_denom = 1 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= 0) and (v >= 0) and (u + v < 1)

def circle_rect_collision(center, radius, rect):
    """Check if circle (center, radius) intersects with rect (x, y, w, h)."""
    # Find the closest point to the circle within the rectangle
    closest_x, closest_y = clamp_point(center, rect)
    
    # Calculate the distance between the circle's center and this closest point
    dist = distance(center, (closest_x, closest_y))
    
    return dist <= radius
