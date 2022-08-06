#current plan 
#just have this draw what is output from GDB but make it pretty 


# class Example(QWidget):

#     def __init__(self):
#         super().__init__()

#         self.initUI()


#     def initUI(self):

#         self.setGeometry(300, 300, 280, 270)
#         self.setWindowTitle('Pen styles')
#         self.show()


#     def paintEvent(self, e):

#         qp = QPainter()
#         qp.begin(self)
#         self.drawLines(qp)
#         qp.end()


#     def drawLines(self, qp):
#         width = 400 
#         height = 400
#         size = 100
#         num_rectangles = 5
#         for i in range(num_rectangles):
#             rectArr = [(width/2)-size,0,(width/2)+size,(i+1)*50]
#             #canvas.create_rectangle(((width/2)-size),0,((width/2)+size),(i+1)*50)
#             pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)

#             qp.setPen(pen)
#         #qp.drawLine(20, 40, 250, 40)
#         #(x0,y0,x1,y1)
#             qp.drawRect(math.floor((width/2)-size),10,math.floor((width/2)+size),(i+1)*50)


from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon, QPainter, QTextDocument
from PyQt6.QtCore import QRect, Qt, QRectF,QPointF,QPoint
import sys
import math 
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Text - Geekscoders.com")
        self.setWindowIcon(QIcon("qt.png"))
        self.setGeometry(500,200, 500,400)
 
    def paintEvent(self, e):
        painter = QPainter(self)
       
        recs = []
        width = 400 
        height = 400
        size = 40
        points = []
        for i in range(5):
            #QRect(xstart, ystart, xsize, ysize)
            recs.append(QRect(100,i*size,100,50))
            #QPointF(x0, y0)
            qpf = QPointF(110,(i*size))
            points.append(qpf)
            #QRect(0)
     
        #draw recteangles
        for r in recs:
           painter.drawRect(r)
        #draw points 
        for p in points:
            painter.drawText(p,"painter text")
   
        
        document = QTextDocument()
       
 
        document.drawContents(painter)
 
 
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())