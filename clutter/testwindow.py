from pprint import pprint
import sys


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
#for l in lines:
#     print(l)
import re

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layouts Example")
        # Create an outer layout
        outerLayout = QVBoxLayout()        
        buttonsLayout = QHBoxLayout()
        button1 = QPushButton("button 1")
        button2 = QPushButton("button 2")
        button3 = QPushButton("button 3")
        button1.setMaximumWidth(100)
        button2.setMaximumWidth(100)
        button3.setMaximumWidth(100)
        blankLabel = QLabel("")
        buttonsLayout.addWidget(button1)
        buttonsLayout.addWidget(button2)
        buttonsLayout.addWidget(button3)
        buttonsLayout.addWidget(blankLabel)

        self.addRegistersCheckBox = QCheckBox("add registers")
        self.addVarsCheckBox = QCheckBox("add Variables")
        self.addFunctionsCheckBox = QCheckBox("add functions")
        #add pmaps/pstat boxes?
        self.addRegistersCheckBox.toggled.connect(self.itemSelected)
        self.addVarsCheckBox.toggled.connect(self.itemSelected)
        self.addFunctionsCheckBox.toggled.connect(self.itemSelected)
        # Create a layout for the checkboxes
        optionsLayout = QVBoxLayout()
        # Add some checkboxes to the layout
        optionsLayout.addWidget(QLineEdit("Option one"))
        optionsLayout.addWidget(QCheckBox("Option two"))
        optionsLayout.addWidget(QCheckBox("Option three"))
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.addRegistersCheckBox)
        hlayout.addWidget(self.addVarsCheckBox)
        hlayout.addWidget(self.addFunctionsCheckBox)
        testcheckbutton = QPushButton("test checked")
        testcheckbutton.clicked.connect(self.testFunc)
        hlayout.addWidget(testcheckbutton)
        # Nest the inner layouts into the outer layout
        outerLayout.addLayout(buttonsLayout)
        outerLayout.addLayout(optionsLayout)
        outerLayout.addLayout(hlayout)
        self.optionsSelected = ""
        # Set the window's main layout
        self.setLayout(outerLayout)
    def testSelected(self):
        print(self.optionsSelected)    
        
    def itemSelected(self):
        value = ""
        if self.addRegistersCheckBox.isChecked():
            value=value+"r"
        if self.addVarsCheckBox.isChecked():
            value=value+"v"
        if self.addFunctionsCheckBox.isChecked():
            value=value+"f"    
        print(value)
        self.optionsSelected = value
        return value      
            
    def testFunc(self):
        pprintOptions = window.optionsSelected
        if pprintOptions.find('r') != -1:
            print("registers to pprint")          
        if pprintOptions.find('v') != -1:
            print("variables to pprint")          
        if pprintOptions.find('f') != -1:
            print("functions to pprint")                  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
