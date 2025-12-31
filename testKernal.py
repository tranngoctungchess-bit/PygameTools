import pygame
import sys
from kernel import Margin
pygame.init()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Kernal 1 - Margin Demo")

# Khởi tạo Margin: Cách lề 5% so với màn hình
margin_system = Margin(screen, percentage_to_screen=(5, 5))

# Vật thể của chúng ta (ví dụ một hình vuông 50x50)
obj_size = (50, 50)
anchors = ['TopLeft', 'TopCenter', 'TopRight', 'Center', 'BottomRight', 'BottomLeft', 'CenterLeft', 'CenterRight', 'BottomCenter']
current_index = 0

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))  # Màu nền tối

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Nhấn SPACE để đổi vị trí Anchor
            if event.key == pygame.K_SPACE:
                current_index = (current_index + 1) % len(anchors)

    # 1. Lấy tên Anchor hiện tại
    current_anchor = anchors[current_index]

    # 2. Dùng class Margin để tính toán vị trí
    pos = margin_system.get_pos(obj_size, current_anchor)

    # 3. Vẽ vật thể (hình vuông màu xanh)
    pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], obj_size[0], obj_size[1]))

    # Hiển thị text hướng dẫn
    font = pygame.font.SysFont(None, 36)
    img = font.render(f"Anchor: {current_anchor} (Press SPACE)", True, (255, 255, 255))
    screen.blit(img, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()