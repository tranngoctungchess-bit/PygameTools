from Kernel import Thread, quitnow, Downlclick, Uplclick, GridLayout, PygameRender, MainScreen
from Kernel.PgRenderCompo import ButtonObj

# Tạo màn hình chính
screen = MainScreen((800,800), bg=(255, 255, 255))
screen.set_caption("Grid Layout Test - 9x9 Color Pattern")

# Tạo GridLayout 9x9
grid = GridLayout(9, 9, (760, 760), (20, 20), padding=5)

# List để lưu tất cả renders
renders = []


# Hàm xử lý cho các button
def create_cell_function(row, col):
    def cell_click():
        print(f"Cell clicked at position ({row}, {col})")

    return cell_click


def cell_release():
    print("Cell released")


# Tạo các button theo grid
for i in range(9):
    for j in range(9):
        # Tạo màu theo quy luật gradient
        red = int(100 + (i * 15))
        green = int(100 + (j * 15))
        blue = 200 - (i * 10)

        hover_red = min(red + 50, 255)
        hover_green = min(green + 50, 255)
        hover_blue = min(blue + 50, 255)

        press_red = max(red - 50, 0)
        press_green = max(green - 50, 0)
        press_blue = max(blue - 50, 0)

        btn_name = f"cell_{i}_{j}"
        btn = ButtonObj.FixedButton(
            parent=screen,
            name=btn_name,
            rect=(grid.cell_width - 10, grid.cell_height - 10),
            bg=(red, green, blue),
            hoverbg=(hover_red, hover_green, hover_blue),
            pressbg=(press_red, press_green, press_blue)
        )

        grid.setpos(btn, (i, j))

        btn.add_vflag(
            (Downlclick, create_cell_function(i, j)),
            (Uplclick, cell_release)
        )

        screen.addWidget(btn, btn_name)

        # Tạo render riêng cho mỗi button và thêm vào list
        btn_render = PygameRender(btn)
        renders.append(btn_render.render)

# Tạo thread với tất cả các renders
game = Thread(screen, renders, quitnow)
game.threadstart()