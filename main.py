import os
import sys
import json 

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QToolBar, QListWidget, QSplitter

def load_json(json_file_path):
    with open(json_file_path, encoding = 'utf-8') as user_file: 
        json_data = json.load(user_file)
        return json_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("org-planner")

app = QApplication(sys.argv)

json_data = load_json("people.json")
list_widget = QListWidget()

all_people_list = json_data["People"]
for i in all_people_list:
    list_widget.addItem(i["Name"])

text_widget = QListWidget()
text_widget.addItem("foo")

splitter_widget = QSplitter()
splitter_widget.addWidget(list_widget)
splitter_widget.addWidget(text_widget)

window = MainWindow()
window.setCentralWidget(splitter_widget)
window.show()

app.exec()
