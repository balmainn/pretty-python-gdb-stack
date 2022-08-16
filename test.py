from pygments import highlight
from pygments.style import Style
from pygments.token import *
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter, HtmlFormatter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import sys


# # Subclass QMainWindow to customize your application's main window


from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

#for l in lines:
#     print(l)
import re
class WindowOne(QMainWindow):

        def __init__(self):
            super(WindowOne, self).__init__()
            self.layout = QGridLayout()
            self.label = QLabel("WINDOW ONE")
            button = QPushButton("BUTTON")
            self.layout.addWidget(self.label)
            self.layout.addWidget(button)
            self.show()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        #self.w = WindowOne()
        
            #styles ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 
            # 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 
            # 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 
            # 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
            # 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 
            # 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 
            # 'dracula', 'one-dark', 'lilypond']
        self.layout = QGridLayout() 
        self.w1 = WindowOne()
        self.w2 = self.WindowTwo()
        self.setWindowTitle(f"multiple Windows")
        button1 = QPushButton("button 1")
        button2 = QPushButton("button 2")
        button1.clicked.connect(self.buttonOneClicked)
        button2.clicked.connect(self.buttonTwoClicked)
        
        self.layout.addWidget(button1,0,0)
        self.layout.addWidget(button2,0,1)
    
        
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
    def buttonOneClicked(self):
        print("button 1 clicked")
        self.w1.show()
        

    def buttonTwoClicked(self):
        print("button 2 clicked")    

    
    class WindowTwo(QWidget):

        def __init__(self):
            #super(MainWindow, self).__init__()
            self.layout = QGridLayout()
            label = QLabel("WINDOW Two")
            self.layout.addWidget(label)
#print(result)

app = QApplication(sys.argv)
#app.setStyleSheet(css)
window = MainWindow()


window.show()

app.exec()
