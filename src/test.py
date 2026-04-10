import pygame
from pgtkb.KernelRun import MainApplication
from pgtkb.PgRenderCompo.TextObj import LineEdit
from pgtkb.UFlags import text_Is_Antialias
from pgtkb import Downlclick

app = MainApplication(
    screen_size=(800, 600),
    screen_bg=(240, 240, 245),
    caption="pgtkb Framework - Dual LineEdit Test",
    fps=60
)

input_username = LineEdit(
    parent=app.screen,
    text_size=28,
    width_line_edit=350,
    pos=(225, 200),
    bg=(255, 255, 255),
    text_color=(40, 40, 40),
    border_color=(100, 100, 200),
    border_width=2,
    border_radius=10,
    pad_x=12,
    pad_y=8,
    name="username_input"
)
input_password = LineEdit(
    parent=app.screen,
    text_size=28,
    width_line_edit=350,
    pos=(225, 300),
    bg=(250, 250, 250),
    text_color=(40, 40, 40),
    border_color=(200, 100, 100),
    border_width=2,
    border_radius=10,
    pad_x=12,
    pad_y=8,
    name="password_input"
)

from pgtkb.PgRenderCompo.TextObj import Label

label_username = Label(
    parent=app.screen,
    color=(60, 60, 80),
    size=20,
    text="Username:",
    pos=(225, 170),
    font="Arial"
)

label_password = Label(
    parent=app.screen,
    color=(60, 60, 80),
    size=20,
    text="Password:",
    pos=(225, 270),
    font="Arial"
)

display_label = Label(
    parent=app.screen,
    color=(80, 80, 100),
    size=18,
    text="Type something...",
    pos=(225, 400),
    font="Arial"
)


def update_display():
    """Hiển thị text từ cả 2 input boxes"""
    username_text = input_username.text if input_username.text else "[empty]"
    password_text = "*" * len(input_password.text) if input_password.text else "[empty]"
    display_label.change_text(f"Username: {username_text} | Password: {password_text}")


app.add_action(update_display)

hint_label = Label(
    parent=app.screen,
    color=(120, 120, 140),
    size=14,
    text="Click on input boxes to type | Press BACKSPACE to delete",
    pos=(225, 450),
    font="Arial"
)

try:
    from pgtkb.PgRenderCompo.ButtonObj import FixedButton


    def clear_all():
        input_username.clear_text()
        input_password.clear_text()
        update_display()
        print("Cleared all inputs!")


    clear_btn = FixedButton(
        parent=app.screen,
        rect=(350, 500, 100, 35),
        bg=(200, 200, 220),
        hoverbg=(180, 180, 200),
        pressbg=(160, 160, 180),
        name="clear_button"
    )
    btn_label = Label(
        parent=clear_btn,
        color=(40, 40, 60),
        size=18,
        text="Clear All",
        pos=(15, 8),
        font="Arial"
    )

    clear_btn.add_vflag((Downlclick, clear_all))

except ImportError:
    print("FixedButton not available, skipping clear button")

if __name__ == "__main__":

    app.threadstart()