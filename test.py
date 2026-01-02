import pygame
from Template.Align.Sun import SunLayout

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Object trung tâm (x, y, width, height)
center_obj = (350, 250, 100, 100)
sun = SunLayout(screen, center_obj, padding=20)

# Test các slot
slots = ['TopCenter', 'BottomCenter', 'LeftCenter', 'RightCenter',
         'TopLeft', 'TopRight', 'BottomLeft', 'BottomRight']

# Kích thước object con
child_size = (60, 40)

# Tính toán và lưu vị trí
positions = {}
for slot in slots:
    try:
        pos = sun.get_pos(slot, child_size)
        positions[slot] = pos
        print(f"{slot}: {pos}")
    except Exception as e:
        print(f"{slot} error: {e}")

# Vẽ để kiểm tra trực quan
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # Vẽ object trung tâm (màu xanh)
    pygame.draw.rect(screen, (0, 120, 255), center_obj, 2)

    # Vẽ các object con (màu đỏ)
    for slot, (x, y) in positions.items():
        pygame.draw.rect(screen, (255, 100, 100), (x, y, *child_size), 2)
        # Hiển thị tên slot
        font = pygame.font.SysFont(None, 24)
        text = font.render(slot, True, (255, 255, 255))
        screen.blit(text, (x, y - 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()