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
        addLabelButton = QPushButton("addLabels")
        removeLabelButton = QPushButton("Remove Labels")
        helpButton =QPushButton("Help")
        #addLabelButton.clicked.connect(self.addLabel)
        #removeLabelButton.clicked.connect(self.removeLabel)

        self.nameLabels = [] 
        self.addressLabels = []
        self.dataLabels = [] 


        # #set the width of the buttons 
        # codeWindowButton.setMaximumWidth(200)
        # button2.setMaximumWidth(100)
        # helpButton.setMaximumWidth(100)
#         for i in reversed(range(numberCurrentLabels-num_needed)):
# #             item = self.labelsLayout.itemAt(i)
# #             item.widget().close()
        align = Qt.AlignmentFlag(0) #align left
        
        self.buttonsLayout.addWidget(addLabelButton,alignment=align)
        
        #codeWindowButton.setMaximumWidth(200)
        
        self.buttonsLayout.addWidget(removeLabelButton,alignment=align)
        self.buttonsLayout.addWidget(helpButton,alignment=align)

        self.outerLayout.addLayout(self.buttonsLayout)
        self.outerLayout.addLayout(self.labelsLayout)
        num_labels = 256 
        self.labelsList = []
        for i in range(num_labels):
            
            testLabel = QLabel(f"{i} test label")
            testLabel2 = QLabel(f"{i} test label")
            testLabel3 = QLabel(f"{i} test label")
            self.labelsList.append(testLabel)
            self.labelsLayout.addWidget(self.labelsList[i],i,0)
            self.labelsLayout.addWidget(testLabel2,i,1)
            self.labelsLayout.addWidget(testLabel3,i,2)
        
        
        #self.gdbOutputText.setFixedWidth(10)
        self.widget.setLayout(self.outerLayout)
        #addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment)
        
        #self.setCentralWidget(widget)
app = QApplication(sys.argv)

window = MainWindow()


window.show()

app.exec()

names = ['a','b','c','d']        
addrs = ['0xaaaa','0xbbbb','0xcccc','0xdddd',]
data= ['adata','bdata','cdata','dData']