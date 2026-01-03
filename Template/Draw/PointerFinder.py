import math


class MissPoint:
    def __init__(self, screen):
        self.screen = screen

    def equilateral_triangle(self, p1, p2):
        """
        Given two points p1, p2, return the third point of an equilateral triangle.
        The triangle is oriented so that the third point is on the left side of vector p1->p2.
        """
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        # Rotate vector by 60° (π/3)
        cos60 = 0.5
        sin60 = math.sqrt(3) / 2
        rx = dx * cos60 - dy * sin60
        ry = dx * sin60 + dy * cos60
        return x1 + rx, y1 + ry

    def parallelogram(self, p1, p2, p3):
        """
        Given three points p1, p2, p3 of a parallelogram (in order),
        return the fourth point p4.
        p4 = p1 + (p3 - p2)
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        return x1 + (x3 - x2), y1 + (y3 - y2)

    def rect_from_diagonal(self, p1, p3):
        """
        Given two opposite corners of a rectangle (diagonal),
        return all four corners in order: (p1, p2, p3, p4).
        """
        x1, y1 = p1
        x3, y3 = p3
        p2 = (x3, y1)  # top‑right
        p4 = (x1, y3)  # bottom‑left
        return p1, p2, p3, p4


    def circle_points(self, center, radius, n):
        """Return n points evenly spaced around a circle."""
        cx, cy = center
        points = []
        for i in range(n):
            angle = 2 * math.pi * i / n
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        return points


    def reflect_point(self, point, line_p1, line_p2):
        """
        Reflect point across the line defined by line_p1 and line_p2.
        """
        x, y = point
        x1, y1 = line_p1
        x2, y2 = line_p2

        # Vector of the line
        dx = x2 - x1
        dy = y2 - y1
        # Square length of the line segment
        seg_len_sq = dx * dx + dy * dy
        if seg_len_sq == 0:
            return point  # line_p1 == line_p2, no reflection

        # Project point onto line
        t = ((x - x1) * dx + (y - y1) * dy) / seg_len_sq
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy

        # Reflect: point = 2 * projection - point
        return 2 * proj_x - x, 2 * proj_y - y