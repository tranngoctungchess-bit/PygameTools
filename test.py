from Template.Align import SFM
import pygame

# Khởi tạo màn hình với Margin 5% ngang và 10% dọc
screen = SFM.MarginScreen(800, 700, (5.0, 10.0))

# Tạo một hình vuông màu đỏ để test
rect_surface = pygame.Surface((100, 100))
rect_surface.fill((255, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Xóa màn hình bằng màu đen
    screen.anchor_render(rect_surface, "Center")

    screen.update()
pygame.quit()