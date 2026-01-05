class VideoResize:
    def __init__(self, screen, tracked_objects=None):
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