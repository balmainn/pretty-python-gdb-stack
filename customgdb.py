#ret here later https://sourceware.org/gdb/onlinedocs/gdb/objfile_002dgdbdotext-file.html#objfile_002dgdbdotext-file
# gdb fs command shows things in windows
#https://cs.brown.edu/courses/cs033/docs/guides/gdb.pdf
import re


class getpid (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(getpid,self).__init__("getpid",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        getpidpy()
getpid() 

class argtest (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(argtest,self).__init__("argtest",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print(arg)
        print(from_tty)
argtest() 
class agt (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(agt,self).__init__("agt",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute(f'argtest, {arg}')
agt() 
#calling argtest from argt doesnt do anything (becaues it doesnt do anything)
#but calling it with gdb.execute the args do get passed 
#also from_tty is false instead of true when calling directly 

def getpidpy():
    out = gdb.execute('info proc files',to_string = True)
    print(out[8:-1])
    pid = out[8:-1]
    return pid

class test (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(test,self).__init__("test",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        pid = getpidpy()
        print("pid from test: ", pid)
test() 


class showcode (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(showcode,self).__init__("showcode",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
       gdb.execute('tui enable')
       gdb.execute('tui')
showcode()
class resource (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("updated source.")
        gdb.execute("source customgdb.py")
        
resource() 

class getFileName (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(getFileName,self).__init__("gfn",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("b main")
        gdb.execute("r")
        out = gdb.execute("info line",to_string = True)
        fileregex = "\".+\""
        m = re.search(fileregex,out)
        filename = m.group(0).strip("\"" )
        print(filename)
   
class myCommand (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(myCommand,self).__init__("cmd",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("b main")
 
class functionInfo (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(functionInfo,self).__init__("fi",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        funcNames, funcNumbers, funcAddrs= getAllFunctions()
        outaddrs = []
        for addr in funcAddrs:
            a = addr[-12:-2]
            outaddrs.append(a)
        for i in range(len(funcNames)):
            print(f"func {funcNames[i]} is on line {funcNumbers[i]} address: {outaddrs[i]}")

functionInfo()
class custumCommand (gdb.Command):
    """user defined gdb command2"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(custumCommand,self).__init__("mycmd",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("r")
        gdb.execute("info registers")

def getFuncAddrs(funcNames):
    funcAddrs = []
    for name in funcNames:
        funcAddrs.append(gdb.execute(f'info address {name}',to_string=True))
    return funcAddrs

def getAllFunctions():
    o = gdb.execute('info functions', to_string = True)
    s = o.splitlines()
    #print(s)
    nbs = 'Non-debugging symbols:'
    ctr = 0
    getFuncNameRE = ' .*\('
    getFuncNumberRE = '.*:'
    for line in s:
        if line == nbs :
            #allstring = s[3:ctr]
            allstring = s[3:ctr-1]
            break
        else:
            ctr=ctr+1    
    #print(allstring)
    funcNumbers = []
    funcNames = []
    funcAddrs = []
    for line in allstring:
        fnumber = re.search(getFuncNumberRE, line).group()
        #print(fnumber)
        funcNumbers.append(fnumber[:-1])
        #print(funcNumbers)
        fname = re.search(getFuncNameRE,line).group()
        #print (fname)
        funcNames.append(fname[1:-1])
        #print(funcNames)
    #breakAllFunctionsByName(funcNames)
    funcAddrs = getFuncAddrs(funcNames)

    return funcNames, funcNumbers, funcAddrs

def breakAllFunctionsByNumber(funcNumbers):
    for num in funcNumbers:
        gdb.execute(f'b {num}')

class firstrun (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(firstrun,self).__init__("firstrun",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        o = gdb.execute("info functions",to_string=True)
        s = o.splitlines()
        print(s)
        nbs = 'Non-debugging symbols:'
        ctr = 0
        getFuncNameRE = ' .*\('
        getFuncNumberRE = '.*:'
        for line in s:
            if line == nbs :
                #allstring = s[3:ctr]
                allstring = s[3:ctr-1]
                break
            else:
                ctr=ctr+1    
        print(allstring)
        funcNumbers = []
        funcNames = []
        funcAddrs = []
        for line in allstring:
            fnumber = re.search(getFuncNumberRE, line).group()
            #print(fnumber)
            funcNumbers.append(fnumber[:-1])
            #print(funcNumbers)
            fname = re.search(getFuncNameRE,line).group()
            #print (fname)
            funcNames.append(fname[1:-1])
            #print(funcNames)
        #breakAllFunctionsByName(funcNames)
            #gdb.execute("b main")
        print(funcNumbers)    
firstrun()         
myCommand()
custumCommand()
getFileName()
# from PyQt6.QtWidgets import (
#       QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
# )
# from PyQt6.QtCore import Qt
# import sys
 
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(300, 250)
#         self.setWindowTitle("CodersLegacy")
 
#         layout = QVBoxLayout()
#         self.setLayout(layout)
 
#         self.label = QLabel("Old Text")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.adjustSize()
#         layout.addWidget(self.label)
 
#         button = QPushButton("Update Text")
#         button.clicked.connect(self.update)
#         layout.addWidget(button)
 
#         button = QPushButton("Print Text")
#         button.clicked.connect(self.get)
#         layout.addWidget(button)
 
#     def update(self):
#         self.label.setText("New and Updated Text")
     
#     def get(self):
#         print(self.label.text())
         
 
# app = QApplication(sys.argv)
# window = Window()
#window.show()
#sys.exit(app.exec())
