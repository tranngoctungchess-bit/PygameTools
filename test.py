import pygame
from Template.Layout.StackLayout import ProVerticalStack

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

stack = ProVerticalStack(screen, (50, 100), reverse=False)

# Thử push 15 object (đủ để wrap)
obj_sizes = [(60, 40)] * 15
positions = []
for i, sz in enumerate(obj_sizes):
    try:
        pos = stack.push(sz, padding=10, wrap=True)
        positions.append(pos)
        print(f"Object {i} placed at {pos}")
    except ValueError as e:
        print(f"Object {i} failed: {e}")
        break

# Vẽ để kiểm tra
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    for rect in stack.objects:
        pygame.draw.rect(screen, (200, 100, 100), rect, 2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()