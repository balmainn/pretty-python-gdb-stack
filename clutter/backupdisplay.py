# # # #https://www.pythonguis.com/tutorials/pyqt6-layouts/
# a python program that takes gdb commands and displays it in that same window. 

#boilerplate 

import sys
 
#from PyQt6.Qt import QApplication, QClipboard
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

import gdb


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.input_returnPressed)
        #self.input.textChanged.connect(gdb.execute(self.input.)self.label.setText)
        self.gdboutput= QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.gdboutput)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def input_returnPressed(self):
        #if input is "this thing" run function "this thing"
        #if input is next or n then run basically everything
        self.label.setText(self.input.text())
        out = gdb.execute(self.input.text(),to_string=True)
        self.gdboutput.setText(out)
        self.input.setText("")
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()



# from PyQt6.QtWidgets import (
#       QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
# )
# from PyQt6.QtCore import Qt
# import sys
 
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 250)
#         self.setWindowTitle("CodersLegacy")
 
#         layout = QVBoxLayout()
#         self.setLayout(layout)
 
#         self.label = QLabel("Old Text")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.adjustSize()
#         layout.addWidget(self.label)
 
#         button = QPushButton("Update Text")
#         button.clicked.connect(self.update)
#         layout.addWidget(button)
 
#         button = QPushButton("Print Text")
#         button.clicked.connect(self.get)
#         layout.addWidget(button)
 
#     def update(self):
#         self.label.setText("New and Updated Text")
     
#     def get(self):
#         print(self.label.text())
         
 
# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())



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