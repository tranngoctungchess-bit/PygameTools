## StackLayout templates

Automatic vertical/horizontal stacking of UI elements.

---

## 1. VerticalStack

Stacks objects vertically (top to bottom by default).
## 2. HorizontalStack
Stacks objects vertically (right to left by default).
### Initialization

```python
from Template.Layout.StackLayout import VerticalStack, HorizontalStack
vstack = VerticalStack(screen, (100, 50))
vstack.push((150, 50), padding=10)
```
## Note
Use reverse=True to stack upward (vertical) or leftward (horizontal).