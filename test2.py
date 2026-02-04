from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

# Tạo label với nội dung khởi tạo
label = QLabel("Chào bạn, mình là QLabel!")
layout.addWidget(label)
window.setLayout(layout)
window.show()
app.exec()