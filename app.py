import os
import sys
import platform
if platform.system() == "Windows":
    import ctypes
    import winreg

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel 

def load_stylesheet(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    print(f"Предупреждение: Файл стиля {file_path} не найден!")
    return ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC_OFFer")
        self.setFixedSize(QSize(550,300))

        if platform.system() == "Windows":
            self.current_theme = None
            self.theme_timer = QTimer(self)
            self.theme_timer.timeout.connect(self.check_system_theme_win)
            self.theme_timer.start(1000)
            self.check_system_theme_win()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(15)

        text = QLabel("А ты всё сохранил или нит?")
        text.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        button = QPushButton("Вырубай")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedSize(160,45)

        button.clicked.connect(self.shutdown_computer)

        layout.addStretch()
        layout.addWidget(text)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

    def shutdown_computer(self):
        current_os = platform.system()

        if current_os == "Windows":
            os.system("shutdown /s /t 0")
        elif current_os == "Darwin":
            mac_cmd = 'osascript -e "do shell script \\"shutdown -h now\\" with administrator privileges"'
            os.system(mac_cmd)
        elif current_os == "Linux":
            os.system("sudo shutdown -h now")

    def check_system_theme_win(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            is_dark_mode = (value == 0)
        except Exception:
            is_dark_mode = False

        if is_dark_mode != self.current_theme:
            self.current_theme = is_dark_mode
            self.update_windows_title_bar(is_dark_mode)

    def update_windows_title_bar(self, is_dark):
            hwnd = int(self.winId())
        
            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                dark_mode = ctypes.c_int(1 if is_dark else 0)
        
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(dark_mode),
                    ctypes.sizeof(dark_mode)
                )
                ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0020)
            except Exception as e:
                print("Не удалось применить темную тему для заголовка:", e)



if __name__ == "__main__":            

    app = QApplication(sys.argv)

    css = load_stylesheet("style.css")
    app.setStyleSheet(css)

    window = MainWindow()

window.show()

app.exec()