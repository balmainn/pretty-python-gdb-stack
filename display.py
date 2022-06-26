
# import re
# gdb.execute('b 4')
# gdb.execute('b 14')
# gdb.execute('b 9')
# gdb.execute('r')
# vars = ['m', 'buff', 't', 'str','end','functionVar']
# for i in range(10):
#     gdb.execute("info locals")
#     for v in vars:
#         try:
#             gdb.execute(f'p &{v}')
#         except:
#             pass
#     gdb.execute('n')


# # #https://www.pythonguis.com/tutorials/pyqt6-layouts/


class resource (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("source display.py")
resource() 


from PyQt6.QtWidgets import (
      QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
import sys
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("CodersLegacy")
 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.label = QLabel("Old Text")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)
 
        button = QPushButton("Update Text")
        button.clicked.connect(self.update)
        layout.addWidget(button)
 
        button = QPushButton("Print Text")
        button.clicked.connect(self.get)
        layout.addWidget(button)

        button = QPushButton("resource")
        button.clicked.connect(self.res)
        layout.addWidget(button)
 
    def update(self):
        filename = "lab01/tracer1a.c"
        with open(filename,'r') as f:
            text = f.readlines()
        # gdb.execute('b main')
        # gdb.execute('r')
        # text = gdb.execute("list",to_string=True)
        t2 = ""
        for t in text:
            t2 = t2 + t
        self.label.setText(f"{t2}")
     
    def get(self):
        print(self.label.text())
    def res(self):
        resource()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())



# # import sys

# # from PyQt6.QtCore import Qt
# # from PyQt6.QtWidgets import (
# #     QApplication,
# #     QCheckBox,
# #     QComboBox,
# #     QDateEdit,
# #     QDateTimeEdit,
# #     QDial,
# #     QDoubleSpinBox,
# #     QFontComboBox,
# #     QLabel,
# #     QLCDNumber,
# #     QLineEdit,
# #     QMainWindow,
# #     QProgressBar,
# #     QPushButton,
# #     QRadioButton,
# #     QSlider,
# #     QSpinBox,
# #     QTimeEdit,
# #     QVBoxLayout,
# #     QWidget,
# # )


# # # Subclass QMainWindow to customize your application's main window
# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()

# #         self.setWindowTitle("Widgets App")

# #         layout = QVBoxLayout()
# #         widgets = [
# #             QCheckBox,
# #             QComboBox,
# #             QDateEdit,
# #             QDateTimeEdit,
# #             QDial,
# #             QDoubleSpinBox,
# #             QFontComboBox,
# #             QLCDNumber,
# #             QLabel,
# #             QLineEdit,
# #             QProgressBar,
# #             QRadioButton,
# #             QSlider,
# #             QSpinBox,
# #             QTimeEdit,
# #             QPushButton,
# #         ]
# #         button = QPushButton("hello world",self)
# #         button.move(100,100)
# #         for w in widgets:
# #             layout.addWidget(w())
# #         layout.addWidget(button)
# #         widget = QWidget()
# #         widget.setLayout(layout)

# #         # Set the central widget of the Window. Widget will expand
# #         # to take up all the space in the window by default.
# #         self.setCentralWidget(widget)


# # app = QApplication(sys.argv)
# # window = MainWindow()
# # window.show()

# # app.exec()




# # # from PyQt6.QtWidgets import *
# # # from PyQt6.QtCore import *
# # # from PyQt6.QtGui import *
# # # import sys
# # # class Color(QWidget):

# # #     def __init__(self, color):
# # #         super(Color,self).__init__()
# # #         self.setAutoFillBackground(True)

# # #         palette = self.palette()
# # #         palette.setColor(QPalette.ColorRole.Window, QColor(color))
# # #         self.setPalette(palette)

# # # class MainWindow(QMainWindow):

# # #     def __init__(self):
# # #         super(MainWindow, self).__init__()

# # #         self.setWindowTitle("My App")

# # #         layout1 = QHBoxLayout()
# # #         layout2 = QVBoxLayout()
# # #         layout3 = QVBoxLayout()
# # #         #setContentsMargins(left,top,right,buttom)
# # #         layout1.setContentsMargins(0,0,50,50)
# # #         layout1.setSpacing(20)

# # #         layout2.addWidget(Color('red'))
# # #         layout2.addWidget(Color('yellow'))
# # #         layout2.addWidget(Color('purple'))

# # #         layout1.addLayout( layout2 )

# # #         layout1.addWidget(Color('green'))

# # #         layout3.addWidget(Color('red'))
# # #         layout3.addWidget(Color('purple'))

# # #         layout1.addLayout( layout3 )

# # #         widget = QWidget()
# # #         widget.setLayout(layout1)
# # #         self.setCentralWidget(widget)
# # # app = QApplication(sys.argv)

# # # #window = QWidget()
# # # #window = QPushButton("button")
# # # window = MainWindow()
# # # window.show()
# # # app.exec()