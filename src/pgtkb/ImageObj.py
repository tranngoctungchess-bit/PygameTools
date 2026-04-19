import pygame
from pgtkb.ObjType import RectTuple, PosTuple
import os
pygame_load = pygame.image.load
convert_alpha = pygame.Surface.convert_alpha
save = pygame.image.save
os_exists = os.path.exists
os_path_join = os.path.join
os_path_splitext = os.path.splitext
def is_image_file(path):
    """Checks if a file path points to a supported image format.

    Args:
        path (str): The file path to check.

    Returns:
        bool: True if the file has a supported image extension, False otherwise.
    """
    ext = os.path.splitext(path)[1].lower()
    return ext in {'.png', '.jpg', '.jpeg', '.bmp', '.gif', 'webp'}

class ImagePack:
    """A wrapper for pygame surfaces to handle image loading and transformations.

    Attributes:
        src (str): The source path of the image.
        surface (pygame.Surface): The underlying pygame surface object.
    """

    def __init__(self, src: str, convert_alpha=True):
        """Initializes the ImagePack with an image from the given source.

        Args:
            src (str): The file path to the image.
            convert_alpha (bool): Whether to convert the surface for alpha transparency.
                Defaults to True.

        Raises:
            ValueError: If the source path is not a valid image file.
        """
        if os_exists(src) and is_image_file(src):
            self.src = src
        else:
            raise ValueError("This is not a valid image path")
        self.surface = pygame_load(src).convert_alpha() if convert_alpha else pygame_load(src)

    def get_rect(self):
        """Returns the bounding rectangle of the image surface.

        Returns:
            pygame.Rect: The rect of the image.
        """
        return self.surface.get_rect()

    def get_size(self):
        """Returns the dimensions of the image surface.

        Returns:
            tuple: A (width, height) tuple.
        """
        return self.surface.get_size()

    def resize(self, size: PosTuple):
        """Resizes the image to the specified size.

        Args:
            size (PosTuple): The target (width, height) for the image.

        Returns:
            ImagePack: The instance itself for method chaining.
        """
        self.surface = pygame.transform.scale(self.surface, size)
        return self

    def scale_resize(self, scale):
        """Resizes the image by a given scale factor.

        Args:
            scale (float): The multiplier for the image dimensions.

        Returns:
            ImagePack: The instance itself for method chaining.
        """
        w, h = self.get_size()
        self.surface = pygame.transform.scale(self.surface, (int(w * scale), int(h * scale)))
        return self

    def rotate(self, angle):
        """Rotates the image by the given angle.

        Args:
            angle (float): The rotation angle in degrees (counter-clockwise).

        Returns:
            ImagePack: The instance itself for method chaining.
        """
        self.surface = pygame.transform.rotate(self.surface, angle)
        return self

    def crop(self, rect: RectTuple):
        """Crops the image to the specified rectangle.

        Args:
            rect (RectTuple): A tuple of (x, y, width, height) representing the crop area.

        Returns:
            ImagePack: The instance itself for method chaining.

        Raises:
            ValueError: If the crop rectangle is out of the image bounds.
        """
        if (rect[0] < 0 or rect[1] < 0 or
                rect[0] + rect[2] > self.surface.get_width() or
                rect[1] + rect[3] > self.surface.get_height()):
            raise ValueError("Crop rectangle out of image bounds")
        else:
            self.surface = self.surface.subsurface(rect)
        return self

    def take_from_crop(self, rect: RectTuple):
        """Returns a copy of a cropped portion of the image without modifying the original.

        Args:
            rect (RectTuple): A tuple of (x, y, width, height) representing the area to copy.

        Returns:
            pygame.Surface: A copy of the specified area.
        """
        return self.surface.subsurface(rect).copy()

    def get_image(self):
        """Returns the underlying pygame Surface object.

        Returns:
            pygame.Surface: The current image surface.
        """
        return self.surface

    def flip(self, horizontal=False, vertical=False):
        """Flips the image horizontally, vertically, or both.

        Args:
            horizontal (bool): Whether to flip horizontally. Defaults to False.
            vertical (bool): Whether to flip vertically. Defaults to False.

        Returns:
            ImagePack: The instance itself for method chaining.
        """
        self.surface = pygame.transform.flip(self.surface, horizontal, vertical)
        return self

    def copy(self):
        """Creates a deep copy of the ImagePack instance.

        Returns:
            ImagePack: A new ImagePack instance with the same source and a copy of the surface.
        """
        new_pack = ImagePack(self.src, convert_alpha=False)
        new_pack.surface = self.surface.copy()
        return new_pack