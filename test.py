from pygments import highlight
from pygments.style import Style
from pygments.token import *
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter, HtmlFormatter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
import sys


# # Subclass QMainWindow to customize your application's main window

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
#for l in lines:
#     print(l)
import re

class HelpDialogue(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("<<TODO> CHANGEME Help Menu!")

        

        QBtn = QDialogButtonBox.StandardButton.Ok 

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        
        
        self.layout = QVBoxLayout()
        message = QLabel("<<TODO>> help menu diag box")
        
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        
        self.setLayout(self.layout)
    def accepted(self):
        self.close()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("<<TODO> CHANGEME!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.diagInput = QLineEdit("enter filename")
        self.diagInput.returnPressed.connect(self.accept)
        
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.layout.addWidget(self.diagInput)
        self.setLayout(self.layout)
    def accept(self):
        #this happens twice when pressing enter for some reason
        text = self.diagInput.text()
        print(text)
        #get filename and save the output here 
    def reject(self):
        print("rejected")    
        self.close()
class CodeWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        
            #styles ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 
            # 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 
            # 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 
            # 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
            # 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 
            # 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 
            # 'dracula', 'one-dark', 'lilypond']
        s = 'vs'
        
        fname = "simple_program.c"
        self.setWindowTitle(f"{fname} Code Window")
        with open(fname,'r') as f:
            code = f.read()
        lexer = CLexer() 
        
        formatter = HtmlFormatter(style=s)
        result = highlight(code, lexer, formatter)
        #print(result)
        css = formatter.get_style_defs()
        self.layout = QGridLayout() 
        
        text2 = [] 
        
     
        lines = css.splitlines()
     
        classesList = []
        colorsList = []
        
        for line in lines:
    #if i > 5:
            color = "<font"
            m = re.split("{|}",line)
            #print(line)
            #print(m[0][1:])
            #print(m[1], m[1][1])
            if(m[1][1]=='f'):
                colorsList.append("")
            else:
                cout = re.sub(': ',"=",m[1])
                color = color+ cout[:-1] +">"
                colorsList.append(color)
            classesList.append(m[0][1:])
            #i = i + 1
        classesList.append("w")
        colorsList.append("<font color=#000000>")
        notFirstRun = False
        for c,color in zip(classesList,colorsList):
            if notFirstRun:
                result = res3
            #c = classesList[i]
            #color = colorsList[i]
            #print(f"class and color : {c[:-1]}, {color}")    
            res = re.sub(f"""<span class="{c[:-1]}">""",color,result)
            res2 = re.sub("</span>","</font>",res)
            notFirstRun = True
            #print(res2)
            #print(i)
            res3 = res2
            #res3 = re.sub("""<span class="w"> +<\/font>""","""  """,res2)
            #res4 = re.sub(f"""<span class="n">""","xxxxxxxxxxx<font>",res3)
            breaktext = QLabel("")
        for line in res3.splitlines():
            label = QLabel("")
            label.setText("\n")
            text2.append(label)
            #print(line)
        
        label2 = QLabel("")    
        label2.setText(res3)
        #self.layout.addWidget(label2,1,1)
        breaknum =14
        bst = ""
        for i in range(len(res3.splitlines())):
            if(i == breaknum):
                bst = bst + f"{i}--->\n"
                
            else:
                bst=bst+f"{i}\n"
        label1 = QLabel("")
        label1.setText(bst)        
        self.layout.addWidget(label1,0,0)
        self.layout.addWidget(label2,0,1)
       
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

       

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
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
        self.w1 = CodeWindow()
        self.w2 = self.WindowTwo()
        self.setWindowTitle(f"multiple Windows")
        codeWindowButton = QPushButton("Show/Hide Code Window")
        button2 = QPushButton("button 2")
        helpButton =QPushButton("Help")
        self.gdbInput = QLineEdit()
        self.gdbInput.returnPressed.connect(self.gdbInputReturnPressed)

        codeWindowButton.clicked.connect(self.codeWindowButtonClicked)
        button2.clicked.connect(self.buttonTwoClicked)
        helpButton.clicked.connect(self.helpButtonClicked)


        self.nameLabels = [] 
        self.addressLabels = []
        self.dataLabels = [] 

        
        num_labels = 10
        for i in range(num_labels):
            nameLabel = QLabel("name label")
            
            addressLabel = QLabel("Address Label")
            dataLabel = QLabel("Data Label")
            self.nameLabels.append(nameLabel)
            self.addressLabels.append(addressLabel)
            self.dataLabels.append(dataLabel)
        for i in range(num_labels):    
            self.nameLabels[i].setStyleSheet("border: 1px solid black;")
            self.addressLabels[i].setStyleSheet("border: 1px solid black;")
            self.dataLabels[i].setStyleSheet("border: 1px solid black;")
            self.labelsLayout.addWidget(self.nameLabels[i],i,0)
            #self.nameLabels[i].setFixedWidth(10)
            self.labelsLayout.addWidget(self.addressLabels[i],i,1)
            self.labelsLayout.addWidget(self.dataLabels[i],i,2)
        for i in range(num_labels):
            self.nameLabels[i].setText(f"{i}name label")


        #set the width of the buttons 
        codeWindowButton.setMaximumWidth(200)
        button2.setMaximumWidth(100)
        helpButton.setMaximumWidth(100)

        align = Qt.AlignmentFlag(0) #align left
        
        self.buttonsLayout.addWidget(codeWindowButton,alignment=align)
        
        #codeWindowButton.setMaximumWidth(200)
        
        self.buttonsLayout.addWidget(button2,alignment=align)
        self.buttonsLayout.addWidget(helpButton,alignment=align)

        self.outerLayout.addLayout(self.buttonsLayout)
        self.outerLayout.addLayout(self.labelsLayout)
        #i dunno about this one 
        self.outerLayout.addWidget(self.gdbInput)
        self.gdbOutputText = QLabel("gdb output goes here")
        self.outerLayout.addWidget(self.gdbOutputText)
        #self.gdbOutputText.setFixedWidth(500)
        
        
        #self.gdbOutputText.setFixedWidth(10)
        self.widget.setLayout(self.outerLayout)
        #addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment)
        
        #self.setCentralWidget(widget)
        #generate the help dialogue box, basically will list commands and what they do (pprint docstring more or less)
    def gdbInputReturnPressed(self):
        text = self.gdbInput.text()
        print(text)    
        self.gdbInput.setText("")
        
        self.gdbOutputText.setText(text)
    def helpButtonClicked(self):
        dlg = HelpDialogue()
        dlg.exec()
    def codeWindowButtonClicked(self):
        print("Code Window clicked")
        if self.w1.isVisible():
            self.w1.hide()
        else:
            self.w1.show()
        

    def buttonTwoClicked(self):
        print("button 2 clicked")    
        
        if self.w2.isVisible():
            self.w2.hide()
        else:
            self.w2.show()
    
    class WindowTwo(QMainWindow):

        def __init__(self):
            super().__init__()
            self.layout = QGridLayout()
            label = QLabel("WINDOW Two")
            label2 = QLabel("WINDOW Two")
            label3 = QLabel("WINDOW Two")
            self.widget = QWidget()
            self.widget.setLayout(self.layout)
            self.scroll = QScrollArea()
            #Scroll Area Properties
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.widget)

            self.setCentralWidget(self.scroll)
            self.layout.addWidget(label,0,0)
            self.layout.addWidget(label3,0,3)
            self.layout.addWidget(label2,0,2)
            self.layout.addWidget(label,0,1)

#print(result)

app = QApplication(sys.argv)

#app.setStyleSheet(css)
window = MainWindow()


window.show()

app.exec()

