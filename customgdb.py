
class myCommand (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(myCommand,self).__init__("cmd",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("b main")
        
class custumCommand (gdb.Command):
    """user defined gdb command2"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(custumCommand,self).__init__("mycmd",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("r")
        gdb.execute("info registers")
 
myCommand()
custumCommand()

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
 
    def update(self):
        self.label.setText("New and Updated Text")
     
    def get(self):
        print(self.label.text())
         
 
app = QApplication(sys.argv)
window = Window()
#window.show()
#sys.exit(app.exec())
