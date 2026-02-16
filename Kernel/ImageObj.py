import pygame
from Kernel.ObjType import MathVal1, MathVal2
import os
pygame_load = pygame.image.load
convert_alpha = pygame.Surface.convert_alpha
save = pygame.image.save
os_exists = os.path.exists
os_path_join = os.path.join
os_path_splitext = os.path.splitext
def is_image_file(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
class ImagePack:
    def __init__(self, src: str, convert_alpha = True):
        if os_exists(src) and is_image_file(src):
            self.src = src
        else:
            raise ValueError("This is not a valid image path")
        self.surface = pygame_load(src).convert_alpha() if convert_alpha else pygame_load(src)
    def get_rect(self):
        return self.surface.get_rect()
    def get_size(self):
        return self.surface.get_size()
    def resize(self, size: MathVal2):
        old_surface = self.surface
        self.surface = pygame.transform.scale(self.surface, size)
        return self
    def scale_resize(self, scale):
        w, h = self.get_size()
        self.surface = pygame.transform.scale(self.surface, (w*scale, h * scale))
        return self
    def rotate(self, angle):
        self.surface = pygame.transform.rotate(self.surface, angle)
        return self
    def crop(self, rect: MathVal1):
        if (rect[0] < 0 or rect[1] < 0 or
                rect[0] + rect[2] > self.surface.get_width() or
                rect[1] + rect[3] > self.surface.get_height()):
            raise ValueError("Crop rectangle out of image bounds")
        else:
            self.surface = self.surface.subsurface(rect)
        return self
    def take_from_crop(self, rect: MathVal1):
        return self.surface.subsurface(rect).copy()
    def get_image(self):
        return self.surface
    def flip(self, horizontal=False, vertical=False):
        self.surface = pygame.transform.flip(self.surface, horizontal, vertical)
        return self
    def copy(self):
        new_pack = ImagePack(self.src, convert_alpha=False)
        new_pack.surface = self.surface.copy()
        return new_pack