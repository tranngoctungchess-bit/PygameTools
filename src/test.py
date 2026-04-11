import pygame
from pgtkb import (
    MainApplication, Label, FixedButton, LineEdit,
    text_Is_Antialias, Anchor, Downlclick
)

# 1. Khởi tạo ứng dụng
# 800x600, màu nền tối cho sang trọng
mainapp = MainApplication(
    (800, 600),
    screen_bg=(30, 30, 45),
    caption="Chương trình sinh nhật pgtkb v23"
)
screen = mainapp.screen

# 2. Thiết lập lề cho toàn bộ màn hình (30px)
screen.set_margin(padding=(30, 30))

# 3. Tiêu đề chính (Căn giữa trên cùng)
title_label = Label(
    screen,
    color=(255, 215, 0),  # Màu vàng Gold
    size=42,
    text="Happy Birthday!",
    Uflags={text_Is_Antialias}
)
title_label.set_margin(padding=(0, 50))  # Cách đỉnh 50px
title_label.push_margin(Anchor.topcenter)

# 4. Ô nhập tên chủ nhân bữa tiệc (Ở chính giữa)
# Test: Con trỏ nhấp nháy, Phím mũi tên, Phím Insert, Phím Enter
name_input = LineEdit(
    screen,
    text_size=28,
    width_line_edit=350,
    pos=(0, 0),  # Vị trí sẽ được push_margin quyết định
    bg=(255, 255, 255),
    text_color=(0, 0, 0),
    border_color=(255, 215, 0),
    border_width=3,
    border_radius=10,
    cursor_color=(255, 0, 0),  # Con trỏ màu đỏ cho nổi
    name="input_birthday_name"
)
name_input.set_margin(padding=(0, 0))
name_input.push_margin(Anchor.center)

# 5. Nhãn hướng dẫn (Nằm dưới ô nhập liệu)
hint_label = Label(
    screen,
    color=(200, 200, 200),
    size=18,
    text="Nhập tên và nhấn ENTER để bắt đầu tiệc",
    Uflags={text_Is_Antialias}
)
# Đặt thủ công dưới ô input một chút
hint_label.change_pos((250, 360))


# 6. Hàm xử lý khi nhấn Enter hoặc nhấn nút Submit
def start_party(widget=None):
    user_name = name_input.text
    if user_name.strip() == "":
        user_name = "Bạn"

    title_label.change_text(f"Tiệc của {user_name} bắt đầu!")
    hint_label.change_text("Sẵn sàng thổi nến chưa nào? 🎂")
    print(f"Khởi động tiệc cho: {user_name}")


# Gán sự kiện Enter cho LineEdit
name_input.on_enter = start_party

# 7. Nút bấm "Bắt đầu" (Căn giữa dưới cùng)
submit_btn = FixedButton(
    screen,
    (200, 50),
    bg=(70, 130, 180),
    hoverbg=(100, 160, 210),
    pressbg=(40, 90, 140),
    name="btn_start"
)
submit_btn.set_margin(padding=(0, 60))  # Cách đáy 60px
submit_btn.push_margin(Anchor.bottomcenter)
submit_btn.add_vflag((Downlclick, start_party))

# Nhãn trên nút bấm
btn_text = Label(
    submit_btn,
    (255, 255, 255),
    20,
    "THỔI NẾN",
    Uflags={text_Is_Antialias}
)
btn_text.set_margin(padding=(0, 0))
btn_text.push_margin(Anchor.center)

# 8. Màn hình chờ (Như yêu cầu của bạn - Bottom Center)
startlabel = Label(
    screen,
    (150, 150, 150),
    16,
    "v0.23 pgtkb - Build with ❤️",
    (text_Is_Antialias,)
)
# Test push_margin cuối cùng
startlabel.set_margin(padding=(0, 10))
startlabel.push_margin(Anchor.bottomcenter)

# CHẠY ỨNG DỤNG
print("Hệ thống pgtkb sẵn sàng. Hãy thử phím INSERT và mũi tên!")
mainapp.threadstart()