import pygame
from Template.Layout.StackLayout import VerticalStack, HorizontalStack

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Test VerticalStack
vstack = VerticalStack(screen, (100, 50), reverse=False)
vstack.push((150, 50), padding=10)
vstack.push((120, 60), padding=10)
print("VerticalStack objects:", vstack.objects)
print("Total length (Vertical):", vstack.total_length)
print("Number of items:", len(vstack))

# Test HorizontalStack
hstack = HorizontalStack(screen, (50, 200), reverse=False)
hstack.push((80, 50), padding=15)
hstack.push((90, 50), padding=15)
print("HorizontalStack objects:", hstack.objects)
print("Total length (Horizontal):", hstack.total_length)
print("Number of items:", len(hstack))

# Test pop
popped = vstack.pop()
print("Popped rect:", popped)
print("Remaining in vstack:", len(vstack))

# Test clear
hstack.clear()
print("After clear, hstack length:", len(hstack))

# Vẽ test (optional)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    # Vẽ các rect từ stacks
    for rect in vstack.objects:
        pygame.draw.rect(screen, (255, 100, 100), rect)
    for rect in hstack.objects:
        pygame.draw.rect(screen, (100, 255, 100), rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()