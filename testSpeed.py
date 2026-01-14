import pygame
import time
import sys


def bench_grid():
    import pygame
    from Kernel.kernel import Grid
    pygame.init()
    screen = pygame.Surface((800, 600))
    grid = Grid(12, 16, screen, (10, 10))

    start = time.perf_counter()
    for _ in range(50000):
        _ = grid.get_cell_rect(5, 7)
    end = time.perf_counter()
    return end - start


def bench_vertical_stack():
    import pygame
    from Template.Layout.StackLayout import VerticalStack
    pygame.init()
    screen = pygame.Surface((800, 600))
    obj_size = (80, 40)
    padding = 10

    start = time.perf_counter()
    for _ in range(5000):
        stack = VerticalStack(screen, (100, 100))
        for __ in range(10):
            stack.push(obj_size, padding)
    end = time.perf_counter()
    total_pushes = 500 * 10
    return end - start


def bench_margin_screen():
    import pygame
    from Template.Align.MarginScreen import MarginScreen
    pygame.init()
    screen = pygame.Surface((800, 600))
    ms = MarginScreen(800, 600, border_percent=(5, 10))
    test_surface = pygame.Surface((100, 50))

    start = time.perf_counter()
    for _ in range(10000):
        ms.anchor_render(test_surface, 'Center')
        ms.anchor_render(test_surface, 'TopRight')
        ms.anchor_render(test_surface, 'BottomLeft')
    end = time.perf_counter()
    calls = 3000
    return end - start


def bench_around_layout_circle():
    import pygame
    from Template.Align.Sun import AroundLayoutPro
    pygame.init()
    screen = pygame.Surface((800, 600))
    pro = AroundLayoutPro(screen, center_obj=(400, 300, 100, 100), padding=10)
    defined_obj = [(60, 40), (70, 50), (80, 30)]

    start = time.perf_counter()
    for _ in range(10000):
        _ = pro.circle(radius=300, defined_obj=defined_obj, angle='auto', padding=5)
    end = time.perf_counter()
    return end - start
def bench_around_layout_get_pos():
    import pygame
    from Template.Align.Sun import AroundLayout
    pygame.init()
    screen = pygame.Surface((800, 600))
    pro = AroundLayoutPro(screen, center_obj=(400, 300, 100, 100), padding=10)
    defined_obj = [100,100]

    start = time.perf_counter()
    for _ in range(10000):
        _ = pro.get_pos('TopRight', defined_obj)
    end = time.perf_counter()
    return end - start
if __name__ == '__main__':
    print("Running performance benchmarks...")
    print(f"Grid.get_cell_rect: {bench_grid():.8f}")
    print(f"VerticalStack.push: {bench_vertical_stack():.8f}")
    print(f"MarginScreen.anchor_render: {bench_margin_screen():.8f}")
    print(f"AroundLayoutPro.circle: {bench_around_layout_circle():.8f}")
    print(f"AroundLayout.get_pos: {bench_around_layout_get_pos():.8f}")
    print("\nSave these numbers for future optimization comparison.")