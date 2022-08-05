
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
import PySide6


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 250)
#         self.setWindowTitle("CodersLegacy")
 
def getData():
    #for now just gets it as a text file
    #when ready slap the arrays from pprint here
    with open ('output.txt', 'r') as f:
        lines=f.readlines()
    linesarr = []
    for line in lines:        
       # print(line.split())
        linesarr.append(line.split())
   # print(linesarr)
    namesarr =[]
    addrsarr = []
    for i in range(len(linesarr)):
        namesarr.append(linesarr[i][0])
        addrsarr.append(linesarr[i][1])

    #print(namesarr,addrsarr)
    for i in range(len(namesarr)):
        print(f"{namesarr[i]} {addrsarr[i]}")
    return namesarr,addrsarr

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon, QPainter, QTextDocument
from PyQt6.QtCore import QRect, Qt, QRectF,QPointF,QPoint
#QString and QRegEXP
import sys
import math 
#from PySide6.QtGui import QSyntaxHighlighter

#PySide6.QtGui.QSyntaxHighlighter.setFormat(start, count, color)
         
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pretty Python GDB Stack - V2")
        self.setWindowIcon(QIcon("qt.png"))
        self.setGeometry(500,200, 500,400)

    def highLight(self,text):
        pass
        #if text == 'esp,ebp,saved_esp,saved_ebp'    
        #well i need to do this anyway, ret here i guess. 
    def paintEvent(self, e):
        outputNames, outputAddrs = getData()
        painter = QPainter(self)

        
        recs = []
        width = 400 
        height = 400
        size = 25
        namePoints = []
        addrPoints = []
        
        #set background color to blue 
        # palette = self.palette()
        # color = 'blue'
        # palette.setColor(QPalette.ColorRole.Window, QColor(color))
        #self.setPalette(palette)
        
        for i in range(len(outputNames)):
            #QRect(xstart, ystart, xsize, ysize)
            recs.append(QRect(100,i*size,100,50))
            #QPointF(x0, y0)
            nameLocationPoint = QPointF(210,(i*size))
            namePoints.append(nameLocationPoint)
            addrsLocationPoint = QPointF(110,(i*size))
            addrPoints.append(addrsLocationPoint)
            #QRect(0)

        #draw recteangles
        for r in recs:
           painter.drawRect(r)
        #draw points 
        # for p in points:
        #     painter.drawText(p,"painter text")
        for i in range(len(outputNames)):
            painter.drawText(namePoints[i],outputNames[i])
            painter.drawText(addrPoints[i],outputAddrs[i])
            painter.setPen(QColor(i*10, i*10, i*10))
        document = QTextDocument()
 
        document.drawContents(painter)
 

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


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