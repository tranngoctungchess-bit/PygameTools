import pygame
class VideoResize:
    """
    VideoResize Module
    ==================

    Module for handling video resize events and managing objects that need to respond to screen size changes.

    This module provides the VideoResize class which tracks objects and notifies them when the video/screen
    is resized, allowing for dynamic UI and game element repositioning.

    Usage
    -----
    1. Initialize the VideoResize module with the main screen and optionally a list of objects to track.
         resize_handler = VideoResize(screen, tracked_objects=[obj1, obj2])
    2. Add or remove objects to be tracked using add_tracked() and remove_tracked() methods.
            resize_handler.add_tracked(new_obj)
            resize_handler.remove_tracked(old_obj)
    3. In the main loop, check for resize events and call the update method if a resize is detected.
            if resize_handler.check_update():
                resize_handler.update()
    4. Objects being tracked should implement either an update_on_resize(screen) method or a handle_event(event) method
       to respond to resize events. The update_on_resize method is called with the new screen object, while handle_event
       receives a VIDEORESIZE event.
    5. Clear all tracked objects if needed using clear_tracked() method.
            resize_handler.clear_tracked()
    """
    def __init__(self, screen, tracked_objects=None):
        """
        Initialize the VideoResize handler.

        Parameters
        ----------
        screen : pygame.Surface or Screen object
            The pygame screen/display object to monitor for size changes.
        tracked_objects : list, optional
            A list of objects to track for resize events. These objects should implement
            either an update_on_resize(screen) method or a handle_event(event) method.
            Default is None, which initializes to an empty list.

        Attributes
        ----------
        screen : pygame.Surface or Screen object
            The screen object being monitored.
        last_size : tuple
            The last known screen size as (width, height).
        tracked : list
            List of objects that will be notified of resize events.
        """
        self.screen = screen
        self.last_size = screen.get_size()
        self.tracked = tracked_objects if tracked_objects else []

    def add_tracked(self, obj):
        self.tracked.append(obj)
    def remove_tracked(self, obj):
        if obj in self.tracked:
            self.tracked.remove(obj)
    def check_update(self):
        current = self.screen.get_size()
        if current != self.last_size:
            self.last_size = current
            return True
        return False

    def update(self):
        for obj in self.tracked:
            if hasattr(obj, 'update_on_resize'):
                obj.update_on_resize(self.screen)
            elif hasattr(obj, 'handle_event'):
                event = pygame.event.Event(pygame.VIDEORESIZE,
                                           w=current[0], h=current[1])
                obj.handle_event(event)
    def clear_tracked(self):
        self.tracked.clear()