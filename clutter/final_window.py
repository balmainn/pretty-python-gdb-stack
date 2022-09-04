
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
import sys

class GDBCodeWindow(QMainWindow):
                    
    def __init__(self):
        #<<TODO>> justification issues here <work on this next <<rethere>> >
        super().__init__()
        #get the filepath for the code window
        #self.getProgramFilePathForCodeWindow()
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.layout = QGridLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        
        self.codeLabels = []
        self.codeInfoLabels = []
        num_labels = 256
        for i in range(num_labels):
            #print("adding line: ",i)
            l = QLabel(f"code_here: {i}")
            self.codeLabels.append(l)
            l = QLabel(f"B ---> : {i}")
            self.codeInfoLabels.append(l)
            
            #self.line_edit2[i].setAlignment(Qt.AlignmentFlag.AlignLeft) 
            
        for j in range(num_labels):
            self.codeLabels[j].setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.codeLabels[j].adjustSize()
            self.layout.addWidget(self.codeInfoLabels[j],j+2,0)
            self.layout.addWidget(self.codeLabels[j],j+2,1)

        updateButton = QPushButton("Update Code")
        #updateButton.clicked.connect(self.updateCodeLabels)

        printButton = QPushButton("Print Text")
        #printButton.clicked.connect(self.get)

        resourceButton = QPushButton("resource")
        #resourceButton.clicked.connect(self.res)
        
        updateGDBButton = QPushButton("update GDB")
        #updateGDBButton.clicked.connect(self.updateGDB)
        testButton = QPushButton("testButton")
        #testButton.clicked.connect(self.testFunc)
        
        self.textStorage = ""
        
        self.line_edit1 = QLineEdit(self)
        #self.line_edit1.move(50, 50)
        #self.line_edit1.returnPressed.connect(self.on_line_edit1_returnPressed)

        #self.line_edit2 = QLabel(self)
        self.nameLabels = []
        self.addrLabels = []
        self.dataLabels = []
        
        for i in range(num_labels):
            print("adding line: ",i)
            nameLabel = QLabel(f"name")
            self.nameLabels.append(nameLabel)
            addrLabel = QLabel(f"addrLabel")
            self.addrLabels.append(addrLabel)
            dataLabel = QLabel(f"dataLabel")
            self.dataLabels.append(dataLabel)
            #self.line_edit2[i].setAlignment(Qt.AlignmentFlag.AlignLeft)                
        
        for i in range(num_labels):
            
            self.layout.addWidget(self.nameLabels[i],i+2,2)
            self.layout.addWidget(self.addrLabels[i],i+2,3)
            self.layout.addWidget(self.dataLabels[i],i+2,4)
            i = i +1
        print("finished adding line edit 2")   
        #self.line_edit2.move(50, 100)

        nextButton = QPushButton("next")
        #nextButton.clicked.connect(self.gdbNext)
        #add the buttons
        self.layout.addWidget(updateButton,0,0)
        self.layout.addWidget(printButton,0,1)
        self.layout.addWidget(resourceButton,0,2)
        self.layout.addWidget(nextButton,0,3)
        self.layout.addWidget(updateGDBButton,0,4)
        self.layout.addWidget(testButton,0,5)
        
        self.layout.addWidget(self.line_edit1,1,0)

        self.widget.setLayout(self.layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        #<<TODO>> resize this
        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('change me later <<TODO>>')



app = QApplication(sys.argv)

window = GDBCodeWindow()
window.show()

app.exec()