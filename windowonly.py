
import sys


# from PyQt6.QtWidgets import (
#       QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMainWindow
# )
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from  PyQt6 import *
import sys
from PIL import Image as Image
from PIL import ImageQt as ImageQt


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 250)
#         self.setWindowTitle("CodersLegacy")
 
class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setGeometry(300, 300, 400, 293)
        self.setWindowTitle('My Widget!')

        width = 400
        height = 300
        img = Image.new(mode = "RGB", size= (width, height))
        img2 = Image.open(img)
        PilImage = img2 #Image.open('kitten.jpg')
        QtImage1 = ImageQt(PilImage)
        QtImage2 = QImage(QtImage1)
        pixmap = QPixmap.fromImage(QtImage2)
        label = QLabel('', self)
        label.setPixmap(pixmap)


if __name__ == '__main__':
    #app = QApplication(sys.argv)
# window = GridMainWindow()
# window.show()
# sys.exit(app.exec())
    app = QApplication(sys.argv)
    myWidget = MyWidget()
    myWidget.show()

    sys.exit(app.exec_())



# # from PyQt6.QtWidgets import (
# #       QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMainWindow
# # )
# from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *
# from PyQt6.QtCore import *
# from  PyQt6 import *
# import sys
 
# class PrintWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # self.left=50
#         # self.top=50
#         # self.width=300
#         # self.height=300
#         self.initUI()
#         textStorage = ""

#     def initUI(self):

#         #self.setGeometry(self.left,self.top,self.width,self.height)
#         layout = QVBoxLayout()
#         self.line_edit1 = QLineEdit(self)
#         #self.line_edit1.move(50, 50)
#         self.line_edit1.returnPressed.connect(self.on_line_edit1_returnPressed)

#         self.line_edit2 = QLabel(self)
#         self.line_edit2.move(50, 100)
#         layout.addWidget(self.line_edit1)
#         layout.addWidget(self.line_edit2)
#         self.show()
#     def updateGDB(self):
#         text = self.textStorage
#         #out = gdb.execute(text,to_string =True)
#         #self.line_edit2.setText(out)

#     def on_line_edit1_returnPressed(self):
#         self.textStorage = self.line_edit1.text()
#         self.line_edit1.setText("")
#         #self.line_edit1.setText(self.line_edit1.text())
#         self.updateGDB()
#         print(self.textStorage)
    
# class Color(QWidget):

#     def __init__(self, color):
#         super(Color, self).__init__()
#         self.setAutoFillBackground(True)

#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor(color))
#         self.setPalette(palette)

# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 250)
#         self.setWindowTitle("CodersLegacy")
 
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.label = QLabel("Old Text")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label.adjustSize()
#         layout.addWidget(self.label)
 
#         button = QPushButton("Update Text")
#         button.clicked.connect(self.update)
#         layout.addWidget(button)
 
#         button = QPushButton("Print Text")
#         button.clicked.connect(self.get)
#         layout.addWidget(button)

#         button = QPushButton("resource")
#         button.clicked.connect(self.res)
#         layout.addWidget(button)
       

  
#     def update(self):
#         filename = "lab01/tracer1a.c"
#         with open(filename,'r') as f:
#             text = f.readlines()

#         t2 = ""
#         for t in text:
#             t2 = t2 + t
#         self.label.setText(f"{t2}")
     
#     def get(self):
#         print(self.label.text())
# from PIL import Image
# from PIL import ImageQt

# width = 400
# height = 300
# img = Image.new(mode = "RGB", size= (width, height))
# iqt = ImageQT(img)
# class GridMainWindow(QMainWindow):

#     def __init__(self):
#         super(GridMainWindow, self).__init__()

#         self.setWindowTitle("My App")

#         layout = QGridLayout()
#         self.label = QLabel(self)
#         self.textEdit = QTextEdit(self)
#         self.lineEdit = QLineEdit(self)
#         pixmap = QPixmap.fromImage(img)
#         self.label.setPixmap(pixmap)
#         layout.addWidget(self.label,0,0)
#         layout.addWidget(self.textEdit,1,0)
#         layout.addWidget(self.lineEdit,1,1)
        
        
#         # layout.addWidget(Color('red'), 0, 0)
#         # layout.addWidget(Color('green'), 1, 0)
#         # layout.addWidget(Color('blue'), 1, 1)
#         # layout.addWidget(Color('purple'), 2, 1)

#         widget = QWidget()
#         widget.setLayout(layout)
#         self.setCentralWidget(widget)

# app = QApplication(sys.argv)
# window = GridMainWindow()
# window.show()
# sys.exit(app.exec())