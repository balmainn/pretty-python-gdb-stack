#current plan for this is to make two windows how we want them then 


# from PyQt6.QtWidgets import (
#       QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMainWindow, QToolBar
# )
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
import sys
import re

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class ProgramWindow(QWidget):
     def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("CodersLegacy")
 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.label = QLabel("ProgramWindow")
        layout.addWidget(self.label)       
        


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.window2 = ProgramWindow()
        
        self.button1 = QPushButton("Push for Window 2")
        self.button1.clicked.connect(
            lambda checked: self.toggle_window(self.window2)
        )
        #file_menu.addAction(button_action)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.button1)
        
        self.resize(300, 250)
        self.setWindowTitle("CodersLegacy")        
        self.label = QLabel("Old Text")
        self.label.setStyleSheet(f'color:{testvar}')
        layout.addWidget(self.label)   
        
        # self.setStatusBar(QStatusBar(self))

        # menu = self.menuBar()

        # file_menu = menu.addMenu("&File")
        # #file_menu.addAction(button_action)
        # file_menu.addSeparator()
        # #file_menu.addAction(button_action2)
        self.window2.show()    
    def toggle_window(self, window):
        if window.isVisible():
            window.hide()
        else:
            window.show()
        self.updateButtonText("Show/hide Window 2")
    def updateButtonText(self,windowState):
        self.button1.setText(windowState)        
if(1):
    app = QApplication(sys.argv)
    #window = PrintWindow()
    testvar = "red"
    window = Window()
    window.show()
    sys.exit(app.exec())

print(sys.argv)    

