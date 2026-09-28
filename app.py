import os
import sys
import platform
if platform.system() == "Windows":
    import ctypes
    import winreg

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel 

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
            self.theme_timer.timeout.connect(self.checkSystemThemeWin)
            self.theme_timer.start(1000)
            self.checkSystemThemeWin()

        self.init_ui()

    def init_ui(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(centralWidget)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(15)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(15)

        text = QLabel("А ты всё сохранил или нит?")
        text.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        buttonShutDown = QPushButton("Вырубай")
        buttonShutDown.setCursor(Qt.CursorShape.PointingHandCursor)
        buttonShutDown.setFixedSize(160,45)

        buttonSleepMod = QPushButton("Спать")
        buttonSleepMod.setCursor(Qt.CursorShape.PointingHandCursor)
        buttonSleepMod.setFixedSize(160,45)

        buttonReboot = QPushButton("Всё по новой")
        buttonReboot.setCursor(Qt.CursorShape.PointingHandCursor)
        buttonReboot.setFixedSize(160,45)

        buttonsLayout.addStretch()
        buttonsLayout.addWidget(buttonShutDown, alignment=Qt.AlignmentFlag.AlignHCenter)
        buttonsLayout.addWidget(buttonSleepMod, alignment=Qt.AlignmentFlag.AlignHCenter)
        buttonsLayout.addWidget(buttonReboot,alignment=Qt.AlignmentFlag.AlignHCenter)
        buttonsLayout.addStretch()

        buttonShutDown.clicked.connect(self.shutDownComputer)

        buttonSleepMod.clicked.connect(self.sleepModComputer)

        buttonReboot.clicked.connect(self.rebootModComputer)

        layout.addStretch()
        layout.addWidget(text)
        layout.addLayout(buttonsLayout)
        layout.addStretch()

    def shutDownComputer(self):
        currentOs = platform.system()

        if currentOs == "Windows":
            os.system("shutdown /s /t 0")
        elif currentOs == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
        elif currentOs == "Linux":
            os.system("sudo shutdown -h now")

    def sleepModComputer(self):
        currentOs = platform.system()

        if currentOs == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif currentOs =="Darwin":
            os.system("osascript -e 'tell app\"System Events\" to sleep'")
        elif currentOs == "Linux":
            os.system("systemctl suspend")

    def rebootModComputer(self):
        currentOs = platform.system()

        if currentOs == "Windows":
            os.system("shutdown /r /t 0")
        elif currentOs == "Darwin":
            os.system("osascript -e 'tell app \"System Events\" to restart")
        elif currentOs == "Linus":
            os.system("systemctl reboot")

    def checkSystemThemeWin(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            is_dark_mode = (value == 0)
        except Exception:
            is_dark_mode = False

        if is_dark_mode != self.current_theme:
            self.current_theme = is_dark_mode
            self.updateWindowsTitleBar(is_dark_mode)

    def updateWindowsTitleBar(self, is_dark):
            hwnd = int(self.winId())
        
            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                darkMode = ctypes.c_int(1 if is_dark else 0)
        
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(darkMode),
                    ctypes.sizeof(darkMode)
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