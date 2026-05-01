from libc.math cimport sqrt, atan2, cos, sin, M_PI, abs as cabs

# Alias for pi
cdef double pi = M_PI

cpdef tuple to_vector(tuple p1, tuple p2):
    """Return the vector from point p1 to point p2."""
    return (p2[0] - p1[0], p2[1] - p1[1])

cpdef double distance(tuple p1, tuple p2):
    """Return the Euclidean distance between two points."""
    cdef double dx = p2[0] - p1[0]
    cdef double dy = p2[1] - p1[1]
    return sqrt(dx*dx + dy*dy)

cpdef object lerp(object a, object b, double t):
    """Linear interpolation between two numbers or points."""
    if isinstance(a, (list, tuple)):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    return a + (b - a) * t

cpdef double dot_product(tuple v1, tuple v2):
    """Return the dot product of two vectors."""
    return <double>v1[0] * <double>v2[0] + <double>v1[1] * <double>v2[1]

cpdef bint is_point_in_circle(tuple point, tuple center, double radius):
    """Check if a point is inside a circle."""
    return distance(point, center) <= radius

cpdef tuple normalize(tuple vec):
    """Return unit vector."""
    cdef double mag = magnitude(vec)
    if mag == 0:
        return (0.0, 0.0)
    return (vec[0] / mag, vec[1] / mag)

cpdef double magnitude(tuple vec):
    """return the distance of two pos"""
    cdef double vx = vec[0]
    cdef double vy = vec[1]
    return sqrt(vx*vx + vy*vy)

cpdef tuple reflect_vector(tuple vec, tuple normal):
    """Reflect a vector across a surface normal (bouncing logic)."""
    cdef tuple n = normalize(normal)
    cdef double dot = dot_product(vec, n)
    return (vec[0] - 2 * dot * n[0], vec[1] - 2 * dot * n[1])

cpdef tuple midpoint(tuple p1, tuple p2):
    """return the pos of the midpoint in the line"""
    return ((p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5)

cpdef tuple point_on_circle(tuple center, double radius, double angle_deg):
    """return position of the point in the circle"""
    cdef double rad = angle_deg * M_PI / 180.0
    return (center[0] + radius * cos(rad),
            center[1] + radius * sin(rad))

cpdef tuple clamp_point(tuple point, tuple rect):
    """Clamp point to be inside rect (x,y,w,h)."""
    cdef double x = point[0]
    cdef double y = point[1]
    cdef double rx = rect[0]
    cdef double ry = rect[1]
    cdef double rw = rect[2]
    cdef double rh = rect[3]
    return (max(rx, min(x, rx + rw)),
            max(ry, min(y, ry + rh)))

cpdef double vector_to_angle(double dx, double dy):
    """Return angle in degrees (0° to 360°) of vector (dx, dy)."""
    cdef double angle_rad = atan2(dy, dx)
    cdef double angle_deg = angle_rad * 180.0 / M_PI
    return angle_deg % 360.0

cpdef object rect_intersection(tuple rect1, tuple rect2):
    """Return overlapping rect as (x, y, w, h), or None if no intersection."""
    cdef double x1 = max(rect1[0], rect2[0])
    cdef double y1 = max(rect1[1], rect2[1])
    cdef double x2 = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
    cdef double y2 = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
    if x2 > x1 and y2 > y1:
        return (x1, y1, x2 - x1, y2 - y1)
    return None

cpdef tuple rotate_point(tuple point, tuple center, double angle_deg):
    """Rotate a point around a center by a given angle (degrees)."""
    cdef double px = point[0], py = point[1]
    cdef double cx = center[0], cy = center[1]
    cdef double rad = angle_deg * M_PI / 180.0
    cdef double cos_a = cos(rad)
    cdef double sin_a = sin(rad)
    cdef double dx = px - cx
    cdef double dy = py - cy
    cdef double rx = dx * cos_a - dy * sin_a
    cdef double ry = dx * sin_a + dy * cos_a
    return (rx + cx, ry + cy)

cpdef double pytagore(double a, double b):
    return sqrt(a*a + b*b)

cpdef double triangle_area(tuple p1, tuple p2, tuple p3):
    cdef double x1 = p1[0], y1 = p1[1]
    cdef double x2 = p2[0], y2 = p2[1]
    cdef double x3 = p3[0], y3 = p3[1]
    return cabs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2.0)

cpdef bint is_point_in_triangle(tuple p, tuple a, tuple b, tuple c):
    cdef double px = p[0], py = p[1]
    cdef double ax = a[0], ay = a[1]
    cdef double bx = b[0], by = b[1]
    cdef double cx = c[0], cy = c[1]

    cdef double v0x = cx - ax, v0y = cy - ay
    cdef double v1x = bx - ax, v1y = by - ay
    cdef double v2x = px - ax, v2y = py - ay

    cdef double dot00 = v0x*v0x + v0y*v0y
    cdef double dot01 = v0x*v1x + v0y*v1y
    cdef double dot02 = v0x*v2x + v0y*v2y
    cdef double dot11 = v1x*v1x + v1y*v1y
    cdef double dot12 = v1x*v2x + v1y*v2y

    cdef double denom = (dot00 * dot11 - dot01 * dot01)
    if denom == 0: return False
    
    cdef double inv_denom = 1.0 / denom
    cdef double u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    cdef double v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    return (u >= 0) and (v >= 0) and (u + v < 1)
