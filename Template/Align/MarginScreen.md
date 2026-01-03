## MarginScreen template

A screen manager with built‑in margin/padding support.  
Automatically positions objects using a 9‑point anchor system.

```python
from Template.Align.MarginScreen import MarginScreen
screen = MarginScreen(800, 600, border_percent=(5, 10))
screen.anchor_render(button_img, 'Center')
```
## Supported Margin
Center, TopCenter, BottomCenter, LeftCenter, RightCenter
TopLeft, TopRight, BottomLeft, BottomRight
## Note
Set resizable=True and call screen.handle_event(event) to handle window resize automatically.