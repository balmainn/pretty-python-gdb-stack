from unicodedata import decimal
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *

import sys
import re 


# class resource (gdb.Command):
#     """reload this file, with changes"""
#     def __init__(self):
#                                  #cmd user types in goeshere
#         super(resource,self).__init__("rs",gdb.COMMAND_USER)
#     #this is what happens when they type in the command     
#     def invoke(self, arg, from_tty):
#         gdb.execute("source test2.py")
# resource() 
import math

class MainWindow(QMainWindow):
                    
    def __init__(self):
        super().__init__()
        #self.w = WindowOne()
        
            #styles ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 
            # 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 
            # 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 
            # 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
            # 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 
            # 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 
            # 'dracula', 'one-dark', 'lilypond']
        self.scroll = QScrollArea() 
        self.widget = QWidget()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.outerLayout = QVBoxLayout()
        self.buttonsLayout = QHBoxLayout()
        self.labelsLayout = QGridLayout() 
        
        
        self.setWindowTitle(f"multiple Windows")

        #addLabelButton.clicked.connect(self.addLabel)
        #removeLabelButton.clicked.connect(self.removeLabel)
        self.red = QSlider(Qt.Orientation.Horizontal, self)
        self.green = QSlider(Qt.Orientation.Horizontal, self)
        self.blue = QSlider(Qt.Orientation.Horizontal, self)
        self.red.setGeometry(30, 40, 200, 30)
        self.green.setGeometry(30, 40, 200, 30)
        self.blue.setGeometry(30, 40, 200, 30)

        #self.outerLayout.addLayout(self.buttonsLayout)
        #self.outerLayout.addLayout(self.labelsLayout)
        self.text ="0xffff some random text here"
        self.redLabel =QLabel("red")
        self.greenLabel =QLabel("green")
        self.blueLabel=QLabel("blue")
        self.button = QPushButton("update label")
        self.redColor ='00'
        self.greenColor = '00'
        self.blueColor = '00'
        self.textlabel = QLabel(self.text)
        self.textlabel.setStyleSheet("font-size: 40pt")
        self.outerLayout.addWidget(self.textlabel)
        self.outerLayout.addWidget(self.redLabel)
        self.outerLayout.addWidget(self.greenLabel)
        self.outerLayout.addWidget(self.blueLabel)

        self.outerLayout.addWidget(self.red)
        self.outerLayout.addWidget(self.green)
        self.outerLayout.addWidget(self.blue)
        
        self.outerLayout.addWidget(self.button)
        self.button.clicked.connect(self.setColorLabel)
        #self.gdbOutputText.setFixedWidth(10)
        self.widget.setLayout(self.outerLayout)

        self.red.valueChanged[int].connect(self.redchangeValue)
        self.blue.valueChanged[int].connect(self.bluechangeValue)
        self.green.valueChanged[int].connect(self.greenchangeValue)
    def setColorLabel(self):
        red = self.getHexValue(self.red.value())
        green = self.getHexValue(self.green.value())
        blue = self.getHexValue(self.blue.value())
        print(red,green,blue)
        # print("red",red,hex(red))
        # print("green",green,hex(green))
        # print("blue",blue,hex(blue))
        out = f"<html><font color=#{red}{green}{blue}>{self.text}</font></html>"
        self.textlabel.setText(out)
    def getHexValue(self,input):
        decimalValue = round(input*255/100)
        if input < 7:
            hexVal = '0'+hex(decimalValue)
            #print(hexVal)
            out = '0'+hexVal[3:]
        else:
            hexVal = hex(decimalValue)
            #print("else hexval",hexVal)
            out = hexVal[2:]
        return out    
    def redchangeValue(self):
        val = self.getHexValue(self.red.value())
        self.redLabel.setText(val)
        red = self.getHexValue(self.red.value())
        green = self.getHexValue(self.green.value())
        blue = self.getHexValue(self.blue.value())
        print(red,green,blue)
        # print("red",red,hex(red))
        # print("green",green,hex(green))
        # print("blue",blue,hex(blue))
        out = f"<html><font color=#{red}{green}{blue}>{self.text}</font></html>"
        self.textlabel.setText(out)
        # red = self.red.value()
        # decimalValue = round(red*255/100)
        # if red < 7:
        #     hexVal = '0'+hex(decimalValue)
        # else:
        #     hexVal = hex(decimalValue)
        # out = '#'+hexVal[2:]
        #print(self.red.value())
        #hexColor = hex(self.red.value())[2:]
        #print(decimalValue, hexVal,out)
        #color = '#'+hex(self.red.value())[2:]+'00'+'00'
        #outText = f"<html><font color={color}>{self.text}</font></html>"
        #self.textlabel.setText(outText)
    def bluechangeValue(self):
        val = self.getHexValue(self.blue.value())
        self.blueLabel.setText(val)
        red = self.getHexValue(self.red.value())
        green = self.getHexValue(self.green.value())
        blue = self.getHexValue(self.blue.value())
        print(red,green,blue)
        # print("red",red,hex(red))
        # print("green",green,hex(green))
        # print("blue",blue,hex(blue))
        out = f"<html><font color=#{red}{green}{blue}>{self.text}</font></html>"
        self.textlabel.setText(out)
    def greenchangeValue(self):
        val = self.getHexValue(self.green.value())
        self.greenLabel.setText(val)
        red = self.getHexValue(self.red.value())
        green = self.getHexValue(self.green.value())
        blue = self.getHexValue(self.blue.value())
        print(red,green,blue)
        # print("red",red,hex(red))
        # print("green",green,hex(green))
        # print("blue",blue,hex(blue))
        out = f"<html><font color=#{red}{green}{blue}>{self.text}</font></html>"
        self.textlabel.setText(out)
    def tfunc(self, instring):
        print(instring)
app = QApplication(sys.argv)

window = MainWindow()


window.show()

app.exec()

names = ['a','b','c','d']        
addrs = ['0xaaaa','0xbbbb','0xcccc','0xdddd',]
data= ['adata','bdata','cdata','dData']