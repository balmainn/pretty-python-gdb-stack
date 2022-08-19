from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
import sys
import re 

class resource (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("source test2.py")
resource() 



gdb.execute("b main")
gdb.execute("r")


def gdbOutWithColor(gdbstring,searchable):
    print("attempting to search the raw string and add color: ",gdbstring)
    regexArr = []
    for addr in searchable:
        regexArr.append("\\b"+addr+"\\b")
    i = 0    
    outst = ""


    for line in gdbstring:
        for regex in regexArr:
            try:
                m = re.search(regex,line)
                if(m):
                    print("m match")
                    print("mspan: ",m.span(0))
                    span = m.span(0)
                    print("matching indicies? : ", line[span[0]:span[1]])
                    
                    outst = outst+"<p>"+line[0:span[0]-1] + "<font color=blue>" + line[span[0]:span[1]] +"</font>" +line[span[1]:]+"</p>\n"
                    #print("outstring? :",outst)
                else: 
                    print(" no match")
            except:
                outst = outst + line
                print("exception?")        
    # for regex in regexArr:
    #     try:
    #         print("attepmting to find: ",regex)   
    #         m = re.search(regex,gdbstring)
        
    #         if(m):
    #             print("m match")
    #             print("mspan: ",m.span(0))
    #             span = m.span(0)
    #             print("matching indicies? : ", gdbstring[span[0]:span[1]])
                
    #             gdbstring = gdbstring[0:span[0]-1] + "<font color=blue>" + gdbstring[span[0]:span[1]] +"</font>" +gdbstring[span[1]:]
    #             #print("outstring? :",outst)
    #         else: 
    #             print(" no match")
    #         i=i+1    
    #     except:
    #         i=i+1
    #         pass     
    return outst    

class MainWindow(QMainWindow):
                    
    def __init__(self):
        super().__init__()

        names = ['aaaa','bbbb','ccccc','ddddd']
        addrs = ['0xaaaa','0xbbbb','0xcccc','0xdddd']
        data = ['a','b','c','d']
        colors = ['red','green','blue','black']

        coloredString = ""
        for i in range(len(names)):
            coloredString = coloredString +f"<p><font color ={colors[i]}>" + names[i]+" " + addrs[i]+" "+data[i] +" " + "</font></p>"
        tabtest = QLabel("")
        tabtext = "<table><thead><tr><th>a1</th><th>b1</th><th>c1</th></tr></thead><tbody><tr><td>a2</td><td>b2</td><td>c2</td></tr></tbody></table>"
                
        #st = gdb.execute("p $sp",to_string =True)
        st = gdb.execute("x/10x $sp",to_string =True)
        arr = ["0xffffcddc","0xffff","0xffffce74", "0xffffce04"]
        #need to put boundries so it only matches the full thing 
        
        gdbout = gdbOutWithColor(st,arr)
        
        #gdbout= "<p>"+gdbout+"</p>"
        print(gdbout)
        
          
        testlabel = QLabel("")
        testlabel.setText(gdbout)
        
        tabtest.setText(tabtext)
        self.scroll = QScrollArea() 
        self.widget = QWidget()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        
        self.layout = QGridLayout() 
        self.widget.setLayout(self.layout)
        self.layout.addWidget(tabtest)
        self.layout.addWidget(testlabel)
        label = QLabel("label")
        label.setText(coloredString)
        self.layout.addWidget(label)


app = QApplication(sys.argv)

#app.setStyleSheet(css)
window = MainWindow()


window.show()

app.exec()
    