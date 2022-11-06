import os
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QToolBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("org-planner")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()