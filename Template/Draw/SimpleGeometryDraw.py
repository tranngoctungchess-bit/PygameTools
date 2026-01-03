#codename: Simple
import pygame


class SimpleDraw:
    def __init__(self, screen):
        self.screen = screen
    def rect(self, rect_info, col=(255,255,255), flags=None):
        if flags is None:
            flags = ['Draw']
        if isinstance(rect_info, pygame.Rect):
            rect = rect_info
        else:
            rect = pygame.Rect(rect_info)
        if 'ReturnPos' in flags:
            pos_data = (rect.x, rect.y, rect.width, rect.height)
        else:
            pos_data = None

        if 'Draw' in flags:
            pygame.draw.rect(self.screen, col , rect)
        return pos_data
    def circle(self, center, radius, col=(255,255,255), flags = None):
        if flags is None:
            flags = ['Draw']
        if 'ReturnPos' in flags:
            pos_data = (radius * 2, radius * 2, center[0] - radius, center[1] - radius)
        else:
            pos_data = None
        if 'Draw' in flags:
            pygame.draw.circle(self.screen, col, center, radius)
        return pos_data
    def triangle(self, p1, p2, p3, col=(255, 255, 255), flags=None):
        if flags is None:
            flags = ['Draw']
        points = [p1, p2, p3]
        if 'ReturnPos' in flags:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            pos_data = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        else:
            pos_data = None
        if 'Draw' in flags:
            pygame.draw.polygon(self.screen, col, points)
        return pos_data

    def line(self, start, end, col=(255, 255, 255), flags=None):
        if flags is None:
            flags = ['Draw']
        if 'ReturnPos' in flags:
            # Bounding rect của đoạn thẳng
            x1, y1 = start
            x2, y2 = end
            pos_data = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        else:
            pos_data = None
        if 'Draw' in flags:
            pygame.draw.line(self.screen, col, start, end)
        return pos_data

    def ellipse(self, rect_info, col=(255, 255, 255), flags=None):
        if flags is None:
            flags = ['Draw']
        if isinstance(rect_info, pygame.Rect):
            rect = rect_info
        else:
            rect = pygame.Rect(rect_info)
        if 'ReturnPos' in flags:
            pos_data = (rect.x, rect.y, rect.width, rect.height)
        else:
            pos_data = None
        if 'Draw' in flags:
            pygame.draw.ellipse(self.screen, col, rect)
        return pos_data