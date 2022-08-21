# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from  PyQt6 import *

# import sys
# import re 

# # class resource (gdb.Command):
# #     """reload this file, with changes"""
# #     def __init__(self):
# #                                  #cmd user types in goeshere
# #         super(resource,self).__init__("rs",gdb.COMMAND_USER)
# #     #this is what happens when they type in the command     
# #     def invoke(self, arg, from_tty):
# #         gdb.execute("source test2.py")
# # resource() 



# # gdb.execute("b main")
# # gdb.execute("r")


# # def gdbOutWithColor(gdbstring,searchable):
# #     print("attempting to search the raw string and add color: ",gdbstring)
# #     regexArr = []
# #     for addr in searchable:
# #         regexArr.append("\\b"+addr+"\\b")
# #     i = 0    
# #     outst = ""


# #     for line in gdbstring:
# #         for regex in regexArr:
# #             try:
# #                 m = re.search(regex,line)
# #                 if(m):
# #                     print("m match")
# #                     print("mspan: ",m.span(0))
# #                     span = m.span(0)
# #                     print("matching indicies? : ", line[span[0]:span[1]])
                    
# #                     outst = outst+"<p>"+line[0:span[0]-1] + "<font color=blue>" + line[span[0]:span[1]] +"</font>" +line[span[1]:]+"</p>\n"
# #                     #print("outstring? :",outst)
# #                 else: 
# #                     print(" no match")
# #             except:
# #                 outst = outst + line
# #                 print("exception?")        
#     # for regex in regexArr:
#     #     try:
#     #         print("attepmting to find: ",regex)   
#     #         m = re.search(regex,gdbstring)
        
#     #         if(m):
#     #             print("m match")
#     #             print("mspan: ",m.span(0))
#     #             span = m.span(0)
#     #             print("matching indicies? : ", gdbstring[span[0]:span[1]])
                
#     #             gdbstring = gdbstring[0:span[0]-1] + "<font color=blue>" + gdbstring[span[0]:span[1]] +"</font>" +gdbstring[span[1]:]
#     #             #print("outstring? :",outst)
#     #         else: 
#     #             print(" no match")
#     #         i=i+1    
#     #     except:
#     #         i=i+1
#     #         pass     
#     #return outst    

# class MainWindow(QMainWindow):
                    
#     def __init__(self):
#         super().__init__()
#         #self.w = WindowOne()
        
#             #styles ['default', 'emacs', 'friendly', 'friendly_grayscale', 'colorful', 'autumn', 
#             # 'murphy', 'manni', 'material', 'monokai', 'perldoc', 'pastie', 'borland', 'trac', 
#             # 'native', 'fruity', 'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 
#             # 'paraiso-light', 'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 
#             # 'rainbow_dash', 'abap', 'solarized-dark', 'solarized-light', 'sas', 'stata', 
#             # 'stata-light', 'stata-dark', 'inkpot', 'zenburn', 'gruvbox-dark', 'gruvbox-light', 
#             # 'dracula', 'one-dark', 'lilypond']
#         self.scroll = QScrollArea() 
#         self.widget = QWidget()
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
#         self.scroll.setWidgetResizable(True)
#         self.scroll.setWidget(self.widget)

#         self.setCentralWidget(self.scroll)
#         self.outerLayout = QVBoxLayout()
#         self.buttonsLayout = QHBoxLayout()
#         self.labelsLayout = QGridLayout() 
        
        
#         self.setWindowTitle(f"multiple Windows")
#         addLabelButton = QPushButton("addLabels")
#         removeLabelButton = QPushButton("Remove Labels")
#         helpButton =QPushButton("Help")
#         addLabelButton.clicked.connect(self.addLabel)
#         removeLabelButton.clicked.connect(self.removeLabel)

#         self.nameLabels = [] 
#         self.addressLabels = []
#         self.dataLabels = [] 


#         # #set the width of the buttons 
#         # codeWindowButton.setMaximumWidth(200)
#         # button2.setMaximumWidth(100)
#         # helpButton.setMaximumWidth(100)

#         align = Qt.AlignmentFlag(0) #align left
        
#         self.buttonsLayout.addWidget(addLabelButton,alignment=align)
        
#         #codeWindowButton.setMaximumWidth(200)
        
#         self.buttonsLayout.addWidget(removeLabelButton,alignment=align)
#         self.buttonsLayout.addWidget(helpButton,alignment=align)

#         self.outerLayout.addLayout(self.buttonsLayout)
#         self.outerLayout.addLayout(self.labelsLayout)
#         num_labels = 256 
#         self.labelsList = []
#         for i in range(num_labels):
            
#             testLabel = QLabel(f"{i} test label")
#             testLabel2 = QLabel(f"{i} test label")
#             testLabel3 = QLabel(f"{i} test label")
#             self.labelsList.append(testLabel)
#             self.labelsLayout.addWidget(self.labelsList[i],i,0)
#             self.labelsLayout.addWidget(testLabel2,i,1)
#             self.labelsLayout.addWidget(testLabel3,i,2)
        
        
#         #self.gdbOutputText.setFixedWidth(10)
#         self.widget.setLayout(self.outerLayout)
#         #addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment)
        
#         #self.setCentralWidget(widget)
        
#     def addLabel(self):
        
#         print("adding label?")
#         inputText = "line1\nline2\n"
#         #num_needed = len(inputText.splitlines())
#         num_needed = 20
#         numberCurrentLabels = self.labelsLayout.count()
#         for i in range(num_needed):
#             if(i < numberCurrentLabels):
#                 item = self.labelsLayout.itemAt(i)
#                 item.widget().setText(f"from added {i}")
#             else:    
#                 addedLabel = QLabel(f"else Label{i}")
#                 self.labelsLayout.addWidget(addedLabel)
#         for i in reversed(range(numberCurrentLabels-num_needed)):
#             item = self.labelsLayout.itemAt(i)
#             item.widget().close()
#         # remove the item from layout
#             self.labelsLayout.removeItem(item)
#     def removeLabel(self):
#         print("removing label")
#         num_needed = 10
#         for i in reversed(range(self.labelsLayout.count()-num_needed)):
#             item = self.labelsLayout.itemAt(i)
#             item.widget().close()
#         # remove the item from layout
#             self.labelsLayout.removeItem(item)
            
        
#     def formatLabelOutput(self, names,addrs,data,colors=[""]):
#         defaultColor = "black"
#         if(len(colors)<2):
#             for i in range(len(names)):
#                 if i == len(colors): 
#                     break
#                 else:
#                     colors.append(defaultColor)
#         outst = "<html>"
#         for i in range(len(names)):
#             spacestring1 = " "
#             spacestring2 = " "
#             outst = outst+f"<p><font color={colors[i]}>"+"<span style= \"border:2px solid black\">"+names[i] +"<span>"+spacestring1 + "<span style= \"border:2px solid black\">"+addrs[i] + "</span>"+spacestring2 + +data[i] + "</span></font></p>"
#         #outst = outst+f"<p><font color={colors[i]}>"+names[i] + spacestring1 + addrs[i] + spacestring2 + data[i] + "</font></p>"
#         outst = outst + "</html>"
#         print(outst)
#         return outst
    

# app = QApplication(sys.argv)

# #app.setStyleSheet(css)
# window = MainWindow()


# window.show()

# app.exec()
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
gdb.execute('r')
out = gdb.execute("frame",to_string = True)
print(out)

