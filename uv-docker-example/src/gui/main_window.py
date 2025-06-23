from PyQt5.QtWidgets import QMainWindow
from src.gui.config.gui_config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, STYLE_SHEET
from src.gui.pages.user_page import UserPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(STYLE_SHEET)
        self.setCentralWidget(UserPage())