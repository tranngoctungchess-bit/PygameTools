import pygame
from pgtkb import (
    MainApplication, FixedButton, Label, LineEdit, Audio,
    Anchor, Border, ToggleButton, ToogleGroup, LayoutHelper,
    CircleButton, CircleToogleButton
)
from pgtkb.VFlags import border, corner_radius, bg_widget
from pgtkb.UFlags import text_Is_Bold

try:
    bgm = Audio("hb.mp3")
    bgm.play(loop=True, volume=0.3)
except Exception as e:
    print("Không có file audio:", e)
def main():
    app = MainApplication(
        screen_size=(800, 600),
        screen_bg=(40, 40, 50),
        caption="Demo pgtkb Build 29",
        fps=60
    )
    screen = app.screen

    # Thiết lập margin để neo các widget
    screen.set_margin(padding=(20, 20))

    # Nhãn tiêu đề
    title = Label(screen, color=(255, 215, 0), size=32, text="Chương trình mẫu Build 29",
                  Uflags={text_Is_Bold})
    title.goto_margin(Anchor.topcenter)

    # Nhóm nút chuyển đổi (chỉ chọn 1)
    group = ToogleGroup(max_button=1)

    # Tạo 3 nút toggle nằm ngang
    btn_data = ["Tab 1", "Tab 2", "Tab 3"]
    btns = []
    layout_helper = LayoutHelper(screen)
    prev_rect = title.get_rect()
    for i, name in enumerate(btn_data):
        btn = ToggleButton(screen, rect=(0,0,100,40),
                           fbg=(70,70,90), tbg=(255,100,100),
                           hoverbg=(100,100,130))
        # Phải set_margin cho btn trước khi con của nó neo
        btn.set_margin(padding=(0,0))
        label = Label(btn, color=(255,255,255), size=16, text=name)
        label.goto_margin(Anchor.center)
        group.add(btn)
        btns.append(btn)

        # Đặt nút bên phải nút trước đó (hoặc title)
        if i == 0:
            pos = layout_helper.getpos_down(prev_rect, btn.get_size(), padding=(10, 10))
        else:
            pos = layout_helper.getpos_right(btns[i-1].get_rect(), btn.get_size(), padding=(5,0))
        btn.change_pos(pos)
        prev_rect = btn.get_rect()

    # Ô nhập liệu
    input_box = LineEdit(screen, text_size=20, width_line_edit=300, pos=(250, 200),
                         bg=(255,255,255), text_color=(0,0,0),
                         border_radius=4, border_width=1, border_color=(200,200,200),
                         name="input")
    # Thêm viền khi focus (có thể dùng callback)
    input_box.add_vflag((border, Border(1, (200,200,200))),
                        (corner_radius, 4))

    @input_box.on_enter()
    def on_send():
        print("Đã nhập:", input_box.text)
        input_box.clear_text()

    # Test CircleButton
    c_btn = CircleButton(screen, center_pos=(100, 400), radius=40,
                         bg=(0, 200, 100), hoverbg=(0, 255, 150), pressbg=(0, 150, 50))
    c_btn.set_margin()
    c_label = Label(c_btn, color=(255, 255, 255), size=14, text="Circle")
    c_label.goto_margin(Anchor.center)

    @c_btn.on_dlclick()
    def on_c_click():
        print("CircleButton clicked!")

    # Test CircleToogleButton with group
    c_group = ToogleGroup(max_button=1)
    
    ct_btn1 = CircleToogleButton(screen, center_pos=(200, 400), radius=40,
                                 fbg=(200, 0, 0), tbg=(255, 255, 255), hoverbg=(255, 100, 100))
    ct_btn1.set_margin()
    ct_label1 = Label(ct_btn1, color=(0, 0, 0), size=14, text="C-Toggle 1")
    ct_label1.goto_margin(Anchor.center)
    c_group.add(ct_btn1)

    ct_btn2 = CircleToogleButton(screen, center_pos=(300, 400), radius=40,
                                 fbg=(0, 0, 200), tbg=(255, 255, 255), hoverbg=(100, 100, 255))
    ct_btn2.set_margin()
    ct_label2 = Label(ct_btn2, color=(0, 0, 0), size=14, text="C-Toggle 2")
    ct_label2.goto_margin(Anchor.center)
    c_group.add(ct_btn2)

    app.event_manager.add_kmod_func(pygame.KMOD_CTRL, (pygame.K_q,), app.immediate_break)

    app.threadstart()

if __name__ == "__main__":
    main()