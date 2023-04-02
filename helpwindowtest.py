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
        helpButton.clicked.connect(self.helpDialogueSpwn)
        #addLabelButton.clicked.connect(self.addLabel)
        #removeLabelButton.clicked.connect(self.removeLabel)

        self.nameLabels = [] 
        self.addressLabels = []
        self.dataLabels = [] 


        align = Qt.AlignmentFlag(0) #align left
        
        self.buttonsLayout.addWidget(addLabelButton,alignment=align)
        
        #codeWindowButton.setMaximumWidth(200)
        
        self.buttonsLayout.addWidget(removeLabelButton,alignment=align)
        self.buttonsLayout.addWidget(helpButton,alignment=align)

        self.outerLayout.addLayout(self.buttonsLayout)
        self.outerLayout.addLayout(self.labelsLayout)
        num_labels = 256 
        self.labelsList = []
        
        #self.gdbOutputText.setFixedWidth(10)
        self.widget.setLayout(self.outerLayout)
        self.hDiag = self.HelpDialogue()
    def tfunc(self, instring):
        print(instring)
    def helpDialogueSpwn(self):
        self.hDiag.show()

    class HelpDialogue(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                
                self.setGeometry(200, 200, 700, 400)
                self.setWindowTitle("Help Dialogue")
        
        
                label = QLabel(self)
                pixmap = QPixmap('ppgdb-help-picture.png')
                label.setPixmap(pixmap)
                QBtn = QDialogButtonBox.StandardButton.Ok 

                self.buttonBox = QDialogButtonBox(QBtn)
                self.buttonBox.accepted.connect(self.accept)
                
                
                self.layout = QVBoxLayout()
                message = QLabel("")
                
                self.layout.addWidget(message)
                self.layout.addWidget(label)
                self.layout.addWidget(self.buttonBox)
                
                self.setLayout(self.layout)    
app = QApplication(sys.argv)

window = MainWindow()


window.show()

app.exec()

names = ['a','b','c','d']        
addrs = ['0xaaaa','0xbbbb','0xcccc','0xdddd',]
data= ['adata','bdata','cdata','dData']