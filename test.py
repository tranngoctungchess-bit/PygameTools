from Kernel import MainApplication, GridLayout
from Kernel.PgRenderCompo.ButtonObj import ToggleButton, ToogleGroup  # Import thêm ToogleGroup

# 1. Khởi tạo App
app = MainApplication(
    screen_size=(800, 800),
    screen_bg=(10, 10, 10),
    caption="Build 22: ToggleGroup 400 Buttons Test"
)

# 2. Tạo ToggleGroup duy nhất cho cả bảng
my_group = ToogleGroup(max_button=3)

grid = GridLayout(20, 20, (760, 760), (20, 20), padding=2)

# 3. Tạo 400 ToggleButtons và thêm vào Group
for i in range(400):
    r, c = divmod(i, 20)
    btn_name = f"t_{r}_{c}"

    # Gradient màu ON
    on_red = int(r * 12.7)
    on_green = int(c * 12.7)

    btn = ToggleButton(
        parent=app.screen,
        name=btn_name,
        rect=(grid.cell_width - 2, grid.cell_height - 2),
        fbg=(30, 30, 30),  # Màu OFF
        tbg=(on_red, on_green, 200),  # Màu ON
        hoverbg=(50, 50, 50)  # Màu Hover
    )

    grid.setpos(btn, (r, c))

    # THÊM NÚT VÀO GROUP
    my_group.add(btn)

    app.screen.addWidget(btn, btn_name)

# 4. Chạy
# Kết quả: Bạn nhấn vào đâu, ô đó sáng, ô cũ tắt.
# 400 nút hoạt động như một khối thống nhất!
app.threadstart()