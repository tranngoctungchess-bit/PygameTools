## VideoResize template

Automatically tracks screen‑size changes and updates registered objects (MarginScreen, Grid, etc.) without manual event handling.

### Why use it?
- Removes boilerplate `VIDEORESIZE` event checks.
- Centralized resize management for multiple UI components.
- Compatible with any object that has `update_on_resize(screen)` or `handle_event(event)`.

### Basic usage
```python
from Template.Collision.VideoResize import VideoResize
from Template.Align.MarginScreen import MarginScreen

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
ui = MarginScreen(800, 600, border_percent=(10, 10), resizeable=True)

vr = VideoResize(screen, [ui])   # track ui

while running:
    # No need to manually check VIDEORESIZE
    if vr.check_update():
        vr.update()   # all tracked objects are adjusted
```
## Methods
add_tracked(obj) – add an object to be updated on resize.

remove_tracked(obj) – stop tracking an object.

check_update() – returns True if screen size changed since last call.

update() – calls update_on_resize or handle_event on all tracked objects.

clear_tracked() – remove all tracked objects.

## Note
Objects are updated only when check_update() returns True.
Call check_update() once per frame in your main loop.