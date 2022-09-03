# # #gdb -q ./simple_program -x t.py 

# # import gdb
# # #from gdb import pretty_printer as pp

# # def get_rbp_and_rip():
# #     pointers = gdb.execute("info frame")
# #     pointer = pointers.s

# # def setbreakpoint():
# #     break_num = app.getEntry("breakpoint")
# #     gdb.execute("b {break_num}")

# # def breakmain():
# #     gdb.execute('b main')

# # def disassemble_main():
# #     o = gdb.execute('disassemble main', to_string=True)
# #     print(len(o))
# # def next ():
# #     o = gdb.execute('n', to_string=True)
# #     print(f"python: {o}")
# #     #print(o)



# # def run():
# #     gdb.execute('r')

# # def quit():
# #     gdb.execute('q')
# # #gdb.execute('file /bin/cat')
# # #o = gdb.execute('disassemble exit', to_string=True)
# # # #print(o)
# # # app = gui("gui name here", "400x200")
# # # app.addButton("next", next)
# # # app.addButton("run", run)
# # # app.addButton("break main", breakmain)
# # # app.addButton("disassemble main", disassemble_main)
# # # app.addButton("quit", quit)
# # # info = ""
# # # app.addTextArea(info)
# # # #sets a breakpoint
# # # #app.addLabelEntry("breakpoint")
# # # #app.addButton("Set Breakpoint", setbreakpoint)
# # # app.go()

# # #gdb.execute('quit')


# # """
# # class HelloComman(gdb.Command):
# #     def __init__(self):
# #         super(HelloCommand, self).__init__("Hello_world", gdb.COMMAND_NONE)

# #     dev invoke(self,filename, from_tty):
# #         #Aquire the GIL
# #             gdb.execute("call PyGILState_Ensure()")
# #             #execute the command
# #             gdb.execute("call PyRun_SimmpleString(\"print(\'hello world\')\")")
# #             #release the GIL 
# #             gdb.execute("call PyGILState_Release(\"$1\")")

# # HelloCommand()
# # """

# # #from pympler import muppy, summary 
# # #all_objects = muppy.get_objects()
# # #summ = summary.summarize(all_objects)
# # #summary.print_(summ)


# # class resource (gdb.Command):
# #     """reload this file, with changes"""
# #     def __init__(self):
# #                                  #cmd user types in goeshere
# #         super(resource,self).__init__("rs",gdb.COMMAND_USER)
# #     #this is what happens when they type in the command     
# #     def invoke(self, arg, from_tty):
        
# #         #gdb.execute("source test.py")
# #         print("test print completed")
# # resource() 
# # import sys,inspect 
# # class test1:
# #     a = 4 
# #     b = 3
# # class two:
# #     t = 3 
# #     a =1
# # #print(sys.modules)
# # for name, obj in inspect.getmembers(sys.modules[__name__]):
# #         if inspect.isclass(obj):
# #             print(obj)


# # names = ['name1','name2','name3','name4']
# # addrs = ['addr1','addr2','addr3','addr4']
# # data = ['data1','data2','data3','data4']
# # colors = ['color1','color2','color3','color4']
# # input = [names,addrs,data,colors]
# # zlist= list(zip(*input))

# # print(zlist)
# # for i in range(len(zlist)):
# #     for j in range(len(zlist[i])):
# #         print(i,j,zlist[i][j])
# #         if j == 3:
# #             color = zlist[i][j]



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
#         self.label = QLabel("label")
#         self.outerLayout.addWidget(self.label)
#         #self.gdbOutputText.setFixedWidth(10)
#         self.widget.setLayout(self.outerLayout)
#         #addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment)
#         self.tfunc()
#         #self.setCentralWidget(widget)
#     def tfunc(self):
                
#         breakpoints = [14,16,22]
#         maxLines = 32
#         currentLine = 22
#         outArr = []
       
#         for i in range(maxLines):
#             outArr.append(i)
#         print(outArr)    
#         for i in range(len(outArr)):
#             innerFound = False
#             for b in breakpoints:
                
#                 if(b == outArr[i] and outArr[i]==currentLine):
#                     outArr[i] = "ba"
#                     innerFound =True
#                     break #continue?
#                 elif(b == outArr[i]):
#                     outArr[i] = 'b'
#                     innerFound =True
#                     break
#             if(not innerFound):
#                 if(i == currentLine):
#                     outArr[i] = "a"
#         outst = ""
#         for i in range(len(outArr)):
#             if str(outArr[i]) =='ba':
#                 outst = outst + "-->B:"+str(i)+"\n"
                
#             elif str(outArr[i]) == 'a':
#                 outst = outst + "-->"+str(i)+"\n"
                
#             elif str(outArr[i]) == 'b':
#                 outst = outst + "B:"+str(i)+"\n"
                
#             else:
#                 outst = outst + str(i)+"\n"
#         print(outst)
#         self.label.setText(outst)
        
# app = QApplication(sys.argv)

# window = MainWindow()


# window.show()

# app.exec()

# names = ['a','b','c','d']        
# addrs = ['0xaaaa','0xbbbb','0xcccc','0xdddd',]
# data= ['adata','bdata','cdata','dData']




import gdb

class ptest (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(ptest,self).__init__("ptest",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        pass
ptest() 
class resource (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        gdb.execute("source t.py")
resource() 
import re
def getCurrentLine():
    if(gdb.selected_inferior().pid):
        out = gdb.execute("frame",to_string = True)
        print(out)
        lines = out.splitlines()
        m = re.search("^\d+", lines[1])
        try:
            numString = m.group(0)#[1:-1]
            numInt = int(numString)
        except:
            numString = 0
            print("error in getCurrentLine")
            pass
    else:
        numString = 0    
    return numString
gdb.execute("b main")
gdb.execute("r")

currentLine = getCurrentLine()
file_path = "simple_program.c" #getprogramfilepath
codeLines = []
with open(file_path, "r") as f:
    codeLines = f.readlines()
print(currentLine)
print(codeLines, len(codeLines))

for i in range(len(codeLines)):
    if i == int(currentLine)-1:
        print("this line matches", i,currentLine,codeLines[i])
    #else: print(i)    