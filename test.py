from Kernel import MainApplication, GridLayout
from Kernel.PgRenderCompo.ButtonObj import ToggleButton

# 1. Khởi tạo App (800x800)
# Nền tối sâu (Deep Dark) để làm nổi bật các ô sáng
app = MainApplication(
    screen_size=(800, 800),
    screen_bg=(15, 15, 15),
    caption="Stress Test: 20x20 Toggle Grid (400 Buttons)"
)

grid = GridLayout(20, 20, (760, 760), (20, 20), padding=2)

# 4. Tạo 400 ToggleButtons
for i in range(400):
    r, c = divmod(i, 20)  # Tính dòng và cột từ 0-19
    btn_name = f"t_{r}_{c}"

    # Tạo hiệu ứng màu Gradient cho trạng thái ON (TrueBg)
    # Màu sẽ chuyển dần từ Xanh Cyan sang Tím Magenta theo tọa độ
    on_red = int(r * 12.7)  # 0 -> 255
    on_green = int(c * 12.7)  # 0 -> 255
    on_blue = 200  # Giữ xanh cố định

    btn = ToggleButton(
        parent=app.screen,
        name=btn_name,
        rect=(grid.cell_width - 2, grid.cell_height - 2),
        fbg=(40, 40, 40),  # Màu khi Tắt (Xám đậm)
        tbg=(on_red, on_green, on_blue),  # Màu khi Bật (Gradient Cyan-Purple)
        hoverbg=(60, 60, 60)  # Màu khi di chuột qua (Xám sáng)
    )

    grid.setpos(btn, (r, c))
    # Thêm vào Screen (MainApplication sẽ tự động Render đệ quy)
    app.screen.addWidget(btn, btn_name)
app.threadstart()