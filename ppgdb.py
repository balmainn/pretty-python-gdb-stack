#<<TODO>>need to add an on_exit button that asks if they want to quit gdb if the window is up. 

from termios import TIOCM_ST
from pygments import highlight
from pygments.style import Style
from pygments.token import *
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter, HtmlFormatter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from termcolor import colored
import sys
import os


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from  PyQt6 import *
#     print(l)
import re
import gdb
gdb.execute('b main')
gdb.execute('r')

#heap class doesnt really do anything right now but may be utilized upon further development of this program.
class Heap:
    def __init__(self) -> None:
        self.heapRegisterAddresses =  []
        self.heapRegisterNames = []
        self.heapBoth = [self.heapRegisterNames,self.heapRegisterAddresses]
        self.heapInit = 0
    def addReg(self, regName, regAddress):
        
        self.heapRegisterAddresses.append(regAddress)
        self.heapRegisterNames.append(regName)
        self.heapInit = 1
    def sortRegs(self):
        regaddrs = self.heapBoth[1]
        reglist = self.heapBoth[0]
        for i in range(len(regaddrs)):
            for j in range(len(regaddrs)):
                # < should be the correct direction
                if int(regaddrs[i],16) < int(regaddrs[j],16):
                # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                    tmpaddrs = regaddrs[i]
                    regaddrs[i] = regaddrs[j]
                    regaddrs[j] = tmpaddrs
                    templist = reglist[i]
                    reglist[i] = reglist[j]
                    reglist[j] = templist
        self.heapBoth.clear()
        self.heapBoth = [reglist, regaddrs]
    def printAll(self):
        print("printing heap")
        for s in self.heapBoth:
            print(s)
        self.sortRegs()
        print("sorted heap")
        for s in self.heapBoth:
            print(s)

#method to print regName and regAdder justified and nice 
def testPrint(names, addrs):
    #print("masterful test print (lol right)")
    print(names, addrs)
    const = 20
    for i in range(len(names)):
        #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
        nameSize = len(names[i])
        spaceString = " "
        for j in range(const-nameSize):
            spaceString = spaceString + " "
        print(f"{names[i]}{spaceString}{addrs[i]}")
   

#the class stack contains all the information about the stack at a given point in the program.
class Stack:
    def __init__(self) -> None:
        #containers that hold register addresses as well as their name (eip, edx, etc.)
        self.stackRegisterAddresses =  []
        self.stackRegisterNames = []
        self.both = [self.stackRegisterNames,self.stackRegisterAddresses]
        #the start and end locations for stack data
        self.dataStart = 0
        self.dataEnd = 0
        #cdefault register color and default special reg color
        self.regColor = 'white'
        self.specialRegColor = 'red'
        self.boundryColor = 'yellow'
        #need to do something with this 
        self.bottomOfStack = "0x00000000"
        #we have not added anything to the stack on creation 
        #this should be used to tell if the stack has been initialized for builder mode (probably?) rethere
        self.stackInit = 0 
        # if(len(self.stackRegisterAddresses) == 0):
        #     self.stackInit == 0
        # else:
        #     self.stackInit == 1

    #function to add registers to their appropriate container 
    def addReg(self, regName,regAddress):
        #print("adding: ",regName, regAddress)
        self.stackRegisterAddresses.append(regAddress)
        self.stackRegisterNames.append(regName)
        self.stackInit = 1
        self.both.clear()
        self.both = [self.stackRegisterNames,self.stackRegisterAddresses]

    def getRegisterPairs(self):
        #if (not self.stackRegisterAddresses):
        #    print("stack registers empty, getting registers")
        self.getRegs()
        boundryList = ["esp", "saved_ebp", "previous_sp"]
        bigListNames = self.stackRegisterNames
        bigListAddrs = self.stackRegisterAddresses
        bigListData = [] 
        #print("addrs and list getregpairs: ", bigListAddrs,bigListNames)
        for i in range(len(bigListAddrs)):
            bigListData.append("")
        if myProgram.mode == "debug":
            for i in range(len(bigListNames)):
                print(f"looking at: {bigListNames[i]} in getPair") 
         #   print(f"bigdata: {i}  {bigListData[i]}")
        #print(len(bigListData))     
            if (bigListNames[i] == 'saved_ebx'):
                    
                for j in range(len(bigListData)):
                    if(bigListNames[j] == 'ebx'):
                        bigListData[i] = 'ebx_'+bigListAddrs[j]
                        bigListData[j] = 'saved_ebx_'+bigListAddrs[i]
                        
                        
                        break

            if (bigListNames[i] == 'saved_eip'):
                #bigListColors[i] = 'magenta' 
                  
                for j in range(len(bigListData)):
                    if(bigListNames[j] == 'eip'):
                        bigListData[i] = 'eip_'+bigListAddrs[j]
                      
                        
                      
            if( bigListNames[i] == 'previous_sp'  ):
                #bigListColors[i] = 'magenta'   
                out = gdb.execute('p $sp',to_string = True)
                try:
                    m = re.search('0x\w+',out)
                    spAddr = m.group(0)
                    bigListData[i] = "$sp_"+spAddr
                except:
                    pass
        if myProgram.mode == "debug":
            print("returning big list data: ",bigListData)        
        return bigListData
    #simple sorting function that sorts the registers by their address.    
    def sortRegs(self):
        
        regaddrs = self.both[1]
        reglist = self.both[0]
        
        for i in range(len(regaddrs)):
            for j in range(len(regaddrs)):
                # < should be the correct direction
                if int(regaddrs[i],16) < int(regaddrs[j],16):
                # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                    tmpaddrs = regaddrs[i]
                    regaddrs[i] = regaddrs[j]
                    regaddrs[j] = tmpaddrs
                    templist = reglist[i]
                    reglist[i] = reglist[j]
                    reglist[j] = templist
        self.both.clear()
        self.both = [reglist,regaddrs]
    
    #prints all stack registers
    def printAll(self):
        if myProgram.mode == "debug":
            print("printing stack")
        regColors =['white'] * len(self.stackRegisterAddresses)        
        printPair(self.stackRegisterNames,self.stackRegisterAddresses,regColors, "")

    def printPretty(self):
        print(f"len self.both: {self.both}")
        names = self.both[0]
        addrs = self.both[1]
        print(f"len names: {len(names)} len addrs {len(addrs)}")
        for i in range(len(names)):
            print(names[i], "\t",addrs[i])
    def getRegs(self):
        
        print('get regs')
        try:
            self.both.clear()
            self.stackRegisterAddresses.clear()
            self.stackRegisterNames.clear()
        #list is already empty so its ok
        except IndexError:
            pass
        
        registers = gdb.execute('info registers',to_string = True)
        regsize = 0
        regs = registers.splitlines()
        for regline in regs:
            line = regline.split()
            name = line[0]
            addr = line[1]
        #    print(name, int(addr,16))
            if(int(addr,16)> int("ffff",16)):
        #        print(f"{regsize} {line} \n")
                self.addReg(name,addr)
                regsize = regsize +1
        
        print("before frame info")
        frameNames, frameRegs = self.getFrameInfo()
        
        print("after frame info")
        #$sp is the same thing as esp
        # spstring = gdb.execute('x $sp',to_string = True)
        # print(spstring[:10])
        # self.addReg("$sp",spstring[:10])
        for i in range(len(frameNames)):
            self.addReg(frameNames[i],frameRegs[i])
        
        #test print
        #print(self.stackRegisterAddresses,self.stackRegisterNames)
        #self.printAll()
        #print("everything added")
    #get important info from the current frame    

    def getFrameInfo(self):
        eip_savedEip_regex = "0x\w+"
        frameStr = gdb.execute('info frame', to_string = True)
        if frameStr == "No Stack":
            return
        frameArr = frameStr.splitlines()
        
        if(0):
            for i in range(len(frameArr)):
                print(i, frameArr[i])
        
        #0th line
        # frame level # is used for recursion 
        m = re.findall(eip_savedEip_regex, frameArr[1])
        #print(m)
        frame_eip = m[0]
        frame_saved_eip = m[1]
        m = re.findall(eip_savedEip_regex, frameArr[3]) #,4,6
        frameRegs = []
        frameRegNames = []
        try: 
            m3 = re.search("argv=\w+",frameArr[3])
            #print("m3group: ", m3.group(0))
            argv = m3.group(0)[5:]
           # print("argv: ", argv)
            frameRegs.append(argv)
            frameRegNames.append("argv")
        except:
            pass
        arglist = []
        if m:
            print(f" arglist m: {m}")
            arglist = m[0]
        #print("11-12char: ",frameArr[4][11:12])
        #if the address is unknown, skip it. 
        stored_locals = []
        previous_sp = []
        #if frameArr[4][11:12] != 'u':
        m = re.findall(eip_savedEip_regex, frameArr[4]) #,4,6
        #print(f"previous sp and stored locals {m} {frameArr[4]}")
        if(len(m)==2):
            stored_locals = m[0]
            previous_sp = m[1]
            print(m)
        if(len(m)==1):
            #stored_locals = m[0]
            previous_sp = m[0]
            print(m)    
        #add saved registers to array!
        m = re.findall(eip_savedEip_regex, frameArr[6]) #,4,6
        #print(m)
        m2 = re.findall("e\D\D ",frameArr[6])

        #print(m2)
        
        for reg in m:
            #print(f"adding: {reg}")
            frameRegs.append(reg)
        
        for reg in m2:
            #print(f"adding name {reg[:-1]}")
            #[:-1] just to get rid of the space at the end. 
            frameRegNames.append("saved_"+reg[:-1])
         
        #print(frameRegs, frameRegNames)
        if frame_eip:
            frameRegs.append(frame_eip)
            frameRegNames.append("frame_eip")
        if frame_saved_eip:
            frameRegs.append(frame_saved_eip)
            frameRegNames.append("saved_eip")
        if arglist:
            frameRegs.append(arglist)
            frameRegNames.append("arglist")
        if stored_locals:
            frameRegs.append(stored_locals)
            frameRegNames.append("stored_locals")
        if previous_sp:
            frameRegs.append(previous_sp)
            frameRegNames.append("previous_sp")
        return frameRegNames, frameRegs

class Func:

    def __init__(self):
        #containers 
        self.functionsName = []
        self.functionsLine = []
        self.functionsAddr = []
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]
        #delete later
        #self.app = QApplication(sys.argv)
        

    #function that retreives all functions from the currently running program
    def getAllFunctions(self):
        o = gdb.execute('info functions', to_string = True)
        s = o.splitlines()
        #print(s)
        #regex soup
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
        funcAddrs = self.getFuncAddrs(funcNames)
        #print("func addrs: ",funcAddrs)
        return funcNames, funcNumbers, funcAddrs
    
    #get the function address    
    def getFuncAddrs(self,funcNames):
        funcAddrs = []
        for name in funcNames:
            out = gdb.execute(f'info address {name}',to_string=True)
        
            m = re.search("0x\w+",out)
            #print("Mgroup: ", m.group(0))
            funcAddrs.append(m.group(0))
        #    print(f"name: {name} out: {out}")
        #print("funcaddrs:", funcAddrs)
        return funcAddrs
    #helper function that populates the function class containers.     
    def populateFunctions(self):
        self.functionsName, self.functionsLine,  self.functionsAddr = self.getAllFunctions()
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]
        #print("populated: ", self.functionsName, self.functionsLine,  self.functionsAddr) 
    
    #print the information stored in the containes (the line the function is on, its name, and its address)
    def printAll(self):
        #convert this into a variable that is easier to understand
      
        print("printing functions")
        names = self.funcInfo[0] 
        addrs = self.funcInfo[2]
        nums = self.funcInfo[1]
        #for now
        #print(self.funcInfo)
        #print("masterful test print (lol right)")
        #print(names, addrs)
        const = 15
        print("---------------------------")
        print("line:function    address")
        print("---------------------------")
        optionalRetString = []
        for i in range(len(names)):
            #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
            nameSize = len(names[i])
            numberSize = len(nums[i])
            spaceString = " "
            for j in range(const-(nameSize+numberSize)):
                spaceString = spaceString + " "
            outst = f"{nums[i]}:{names[i]}{spaceString}{addrs[i]}"    
            print(outst)
            optionalRetString.append(outst)
        return optionalRetString
    def funcSortByNumber(self):
        names = self.functionsName
        lines = self.functionsLine
        addrs = self.functionsAddr
        if len(lines)<2:
            print("only one function nothing to do.")
            return
        #print("before sorting:", lines)
        for i in range(len(names)):
            for j in range(len(names)):
                if(int(lines[i])< int(lines[j])):
                    
                    temp = lines[i]
                    lines[i] = lines[j]
                    lines[j] = temp

                    temp = names[i]
                    names[i] = names[j]
                    names[j] = temp

                    temp = addrs[i]
                    addrs[i] = addrs[j]
                    addrs[j] = temp
        #print("after sorting:",lines)  
    def funcSortByNameLength(self):
        names = self.functionsName
        lines = self.functionsLine
        addrs = self.functionsAddr
        if len(lines)<2:
            print("only one function nothing to do.")
            return
        #print("before sorting:", lines)
        for i in range(len(names)):
            for j in range(len(names)):
                if(len(names[i])< len(names[j])):
                    
                    temp = lines[i]
                    lines[i] = lines[j]
                    lines[j] = temp

                    temp = names[i]
                    names[i] = names[j]
                    names[j] = temp

                    temp = addrs[i]
                    addrs[i] = addrs[j]
                    addrs[j] = temp
        #print("after sorting:",lines)            
class Variables:
    def __init__(self):  
        #containers
        self.varNames = []
        self.varAddrs = []
        self.varDatas = []
        self.variableInfo = [self.varNames,self.varAddrs,self.varDatas]
    def updateVariableInfo(self):
        self.variableInfo = [self.varNames,self.varAddrs,self.varDatas]
    #sorting variables by their address 
    def sort(self):
        #print('sorting')
        #print(self.varAddrs)
        regaddrs = self.varAddrs
        reglist = self.varNames
        datas = self.varDatas
        for i in range(len(regaddrs)):
            for j in range(len(regaddrs)):
                # < should be the correct direction
                if int(regaddrs[i],16) < int(regaddrs[j],16):
                # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                    tmpaddrs = regaddrs[i]
                    regaddrs[i] = regaddrs[j]
                    regaddrs[j] = tmpaddrs
                    templist = reglist[i]
                    reglist[i] = reglist[j]
                    reglist[j] = templist
                    tempdata = datas[i]
                    datas[i] = datas[j]
                    datas[j] = tempdata
        
    #print the variables and their information    
    def printAll(self):
        print("printing variables")
        const = 10
        spacestring2 = "     "
        print("name         address      data")
        for i in range(len(self.varNames)):
            spaceString = " "
            nameSize = len(self.varNames[i])
            for j in range(const-nameSize):
                spaceString = spaceString + " "
            #print(self.varNames[i], self.varAddrs[i], self.varDatas[i])
            print(f"{self.varNames[i]}{spaceString}{self.varAddrs[i]}{spacestring2}{self.varDatas[i]}")
    #<<TODO>>    
    def getVariableType(varstring):
        #if(varString ==)
        pass
    #function obtains all variable names, addresses, and data in the current frame
    #in addition to all variables that the running program might use. 
    #this will gather whatever information is there, garbage or not. Overflow or not. 
    #this is intended behavior. 
    def getGlobalVariables(self):
        print("getGlobalVariables")
        out = gdb.execute('info variables', to_string = True)
        globalVarRegex = "\w+;$"
        lines = out.splitlines()
        globalvarnames = []
        #variable names
        for line in lines:
        #print(line)
            try:
                m = re.search(globalVarRegex,line)
            #    print(m.group(0))
                globalvarnames.append(m.group(0))
                self.varNames.append(m.group(0))
            except:
                pass
        #m = re.findall(globalVarRegex,out)
        m = re.search(globalVarRegex,out)
        print(m.group(0))
        for var in m:
            print(var[-1:])
    def getLocalVariables(self):
        self.varNames.clear()
        self.varAddrs.clear()
        self.varDatas.clear()
        #self.getGlobalVariables()
        #variable names are the first grouping of "words" at the beginning 
        out = gdb.execute('info locals', to_string = True)
        out2 = gdb.execute('info variables', to_string = True)
        globalVarRegex = "\w+;$"
        localVariableNames = []
        localVarAddresses = []
        variableRegex = "^\w+"
        lines = out.splitlines()
        #variable names
        for line in lines:
        #print(line)
            try:
                m = re.search(variableRegex,line)
                localVariableNames.append(m.group(0))
                self.varNames.append(m.group(0))
            except:
                pass
        lines = out2.splitlines()    
        for line in lines:
        #print(line)
            try:
                m = re.search(globalVarRegex,line)
                print(m.group(0)[:-1])
                localVariableNames.append(m.group(0)[:-1])
                self.varNames.append(m.group(0)[:-1])
                
            except:
                pass
            #print(variableNames)
        for var in localVariableNames:
            out = gdb.execute(f"print &{var}",to_string = True)
            m = re.search('0x\w+',out)
            v = m.group(0)
            localVarAddresses.append(v)
            self.varAddrs.append(v)
            
        for var in localVariableNames:
            #try and read the data value of the variable, if it cant set to null
            #null means the varaible has not been instanciated yet, most likely because the program just started
            try:
                #variable type with whatis
                #out = gdb.execute(f"whatis {var}",to_string = True)
                #self.getVariableType()
                #print(f"{var}: {out}")
                out = gdb.execute(f"print {var}",to_string = True)
                o = out.split()
                #o = o.replace("'",'')
                #print(f"{var}: {out} o:{o} len: {len(o)}")
                datast = ""
                if(len(o)>3):
                    #remove ' and " characters
                    d1 = o[3].strip('\"')
                    datast =d1.replace("'",'')
                    print("this is a character")
                 #   print(print(f"{var}: {o[3][0]}"))
                else:
                    #remove ' and " characters
                    d1 = o[2].strip('\"')
                    if(not myProgram.window.w1.isVisible()):
                        datast =d1.replace("'",'')
               #dont add data that has has not been initialized yet. 
                print(f"datast: {datast}")
                if(datast=='<error:'):
                    self.varDatas.append('null')    
                #<incomplete questionable <<TODO>>
                # if(datast=='<incomplete'):
                #     self.varDatas.append('memory')        
                #print(f"the datast for {var}: {datast} 0th_char: {datast[0]}")  
                else: 
                    self.varDatas.append(datast)
            except gdb.MemoryError:
                #print("some memerror, ignoring")
                self.varDatas.append('null')
        #dont need to return...?
        return localVariableNames, localVarAddresses

    #this will gather all of the variables for the entire program, but not the data.
    def gatherAllVariables():
        
        allVariableNames = []
        allVariableAddresses = []

            #for each function get its variables
        for i in range(len(funcNames)):
            try:
                localVariableNames = []
                localVarAddresses = []
                localVariableNames, localVarAddresses = self.getLocalVariables()
                #print(allVariableNames, allVariableAddresses)
                #append local variables to all variables
                for i in range(len(localVariableNames)):
                    allVariableAddresses.append(localVarAddresses[i])
                    allVariableNames.append(localVariableNames[i])
                    #print(localVariableNames[i], localVarAddresses[i] )

                gdb.execute('c')
            except:
                pass
        return allVariableNames, allVariableAddresses
    #print all of the variable names along with their addresses
    def printAllVars(self):
        allVariableNames = self.varNames
        allVariableAddresses = self.varAddrs
        for i in range(len(allVariableNames)):
            print( allVariableNames[i], allVariableAddresses[i])
    
    #update the location of the variable on the stack regardless of whether or not it has actually moved. 
    def updateVariables(allVariableNames,allVariableAddresses):
        #for var in allVariableNames:
        for i in range(len(allVariableNames)):
            var = allVariableNames[i]
            try:
            # print({var})
                out = gdb.execute(f"print &{var}",to_string = True)
                #print(out)
                #either -11 or -9
                v = out[-9:].strip()
            # print(f"v {v}")
                #this should still be fine, because indicies never change for this array
                #because i'm going to clobber the updated array every time i use it anyway
                #bad performance but its fine for right now. 
                
        #if variables are missing this is probably why.
        #performance, yes, stability.... TBD
                if (allVariableAddresses[i] != v):
                    print(f"changing {allVariableNames[i]} {allVariableAddresses[i]} to {v}")
                    allVariableAddresses[i] = v

            except gdb.error:
                #print(f"{var} not in scope, nothing to do")
                pass
        return allVariableNames, allVariableAddresses
#gdb command for printing all variables       
class pvars (gdb.Command):
    """find and print the variables known at the current point"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pvars,self).__init__("pvars",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        if(isGDBRunningpy()):
            #if(not myProgram.window.isVisible()):
            print("invoking pvars")
            myProgramVariables.getLocalVariables()
            
            if(from_tty):
                if(not myProgram.window.isVisible()):
                    myProgramVariables.printAll()
            #this may need to be elif later or need to double check from_tty
            else:
                    print("updating gdb window pvars")
                    #print(myProgramVariables.variableInfo)
                    #myProgramVariables.updateVariableInfo()
                    #print(myProgramVariables.variableInfo)
                    colors = []
                    for i in range(len(myProgramVariables.varNames)):
                        colors.append("blue")

                    lst = [myProgramVariables.varNames,myProgramVariables.varAddrs,myProgramVariables.varDatas]
                    #lst = [myProgramVariables.varNames,myProgramVariables.varAddrs,myProgramVariables.varDatas,colors]

                    argString = arg.strip('').split('-')
                    if(myProgramWindow.isVisible() and argString[0] != 'from_pprint'):
                        print(lst)
                        myProgramWindow.changeCentralLabels(lst)

                    
            #myProgramVariables.sort()
            #myProgramVariables.printAll()
        else:
            print("not debugging, please run before using.")
pvars() 

def pvartest(input,givenColors=0):
    print("pvartest")
    if(givenColors):
        pass
    else:
        zlist = list(zip(*input))
        for i in range(len(zlist)):
            out = ""
            for componant in zlist[i]:
                out = out + componant +" "
        #print(zlist)
            print(out)
            #self.centralLabels.setText(out)
        pass
    

class Program:

    def __init__(self):   
        
        #programs have a stack, a heap, functions, and variables.
        self.programStack = Stack()
        self.programHeap = Heap()
        self.programFuncs = Func()
        self.programVariables = Variables()
        self.app = QApplication(sys.argv)
        
        
        self.window = self.MainWindow()
        self.codeWindow = self.window.w1
        

        #mode the program runs in (should initialze to something)
        #simple / default are the same thing
        #self.mode = ""
        self.mode = "default"
        #default colors
        #variables
        self.varColor = "green"
        #functions
        self.funcColor = "blue"
        #used for stack
        self.regColor = self.programStack.regColor

        #special registry colors (esp, edi, etc)
        self.specialRegisterColor = self.programStack.specialRegColor
        self.defaultColor = "white"

        self.programMode = ""
        #the executable and filepath of the program.
        #this is somefile
        self.executable =""
        #this is somefile.c
        self.filepath = ""
        #PID = getPID()
        
        #arrray of functions... 
        #program's process ID 
        self.PID = 0
        
        self.variableNames = []
        self.variableAddresses = []
        self.variableBoth = [self.variableNames,self.variableAddresses]
        #things from proc/<pid>/stat
        self.dataStart = 0
        self.dataEnd = 0
        self.bottomOfStack = "0x00000000"
        self.argstart = 0
        self.argend = 0
        self.heapexpand = 0
        self.statHexInfo = []
        self.statWhatInfo = []

        #from proc/<pid>/maps
        self.mapHeapBottom = 0 
        self.mapHeapTop = 0 
        self.mapStackBottom = 0
        self.mapStackTop = 0
        #this might be a bad idea...
        #sizes [2], [2], [3], [3]
        self.everything = [ [self.programHeap.heapBoth], [self.programStack.both], [self.programFuncs.functionsAddr], [self.variableBoth]   ]
        self.trackStacks = []
        print("__init__")
        #retrieve the program's PID, filepath, and executable path. 
        self.getPID()
        self.filepath = "unknown.c"
        self.executable = "unknown"
        self.getProgramFilePath()
        self.sortedAddrs = [] 
        self.sortedNames = []
        self.sortedColors = []
        self.sortedData = []
    def addSorted(self, ssortedAddrs, ssortedNames, sortedColors):
        print(f"insorted: {ssortedAddrs}")
        for a in ssortedAddrs:
        
            self.sortedAddrs.append(a)
        for n in ssortedNames:
            self.sortedNames.append(n)
        self.sortedColors = sortedColors
  
    #change the output color.
    def changeColor(self, color, t):
        print(f"recieved: {color} {t}")
        try: 
            out = "changing " +colored(t,color) + " to " + colored(color,color)
            

            if(t=="var" or t == 'variable'):
                self.varColor = color
            elif(t == 'func' or t== 'function'):
                self.funcColor = color
            elif(t == 'reg' or t == 'register'):
                print("changing registers")
                self.regColor = color
                return
            elif(t == 's' or t== 'specialreg'):
                self.specialRegisterColor = color
            else:
                print(f"invalid input: {t}")
            
        except KeyError:
            print(f"invalid color option {color}")
            
        print(out)
    #get the program filepath
    def getProgramFilePath(self):
        line = gdb.execute('info file', to_string = True)
        fpre = "`\/home\/.+'"
        try:
            m = re.search(fpre,line)
            self.filepath = m.group(0)[1:-1]
            self.executable = self.filepath
            self.filepath = self.filepath+".c"
        except:
            self.filepath = "unknown.c"
            self.executable = "unknown"
            pass
            
        localfilepath = self.executable
        try:
            m = re.search("\w+$",localfilepath)
            localfilepath = m.group(0)
            
        except:
            localfilepath = "unknown.c"
            pass
        if(self.filepath == "unknown.c" or localfilepath == "unknown.c"):
            print("cannot parse this file, is it named correctly?")  
            return  
        self.localexecutable = localfilepath
        self.localfilepath = localfilepath+".c"
        print(self.filepath) 
        
    #get the running program's process ID
    #this starts debugging leaving it on the first line of main. 
    def getPID(self):
        #gdb.execute('b main')
        #gdb.execute('r')
        out = gdb.execute('info proc files',to_string = True)
        print(out[8:-1])
        pid = out[8:-1]
        self.PID = pid
    #<<TODO>> sort all of these things (maybe just use sorthebiglist or something)    
    def sortAll(self):
        #sort these methods
        self.everything = [ [self.programHeap.heapBoth], [self.programStack.both], [self.programFuncs.functionsAddr], [self.variableBoth]   ]

    #retrieve things from /proc/$PID/stat
    def getThingsFromStat(self):
        
        procnospace = isGDBRunningpy()
        if(not procnospace):
            print("gdb is not running, please run before using this function")
            return
        #original information 
        #useful_stack_info = [23,26,27,28,29,30,45,46,47,48,49,50,51,52]
        #whatInfo = ["vsize","startcode","endcode", "startStack", "currentESP", "currentEIP", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"]
        useful_stack_info = [23,26,        27,           28,         45,        46,         47,         48,         49,           50,      51,       52]
        whatInfo = ["vsize","startcode","endcode", "startStack", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"]
        info = []
        hexinfo = []
        command1 = f"cat /proc/{procnospace}/stat | awk "
        command2 = "\' {print "
        #initialize to #26 for no reason
        command3 = f"${useful_stack_info[1]}"    
        command4 = " } \' "
        command_out = command1 + command2 +command3 +command4 
        #print(command_out)
        for location in useful_stack_info:
            command3 = f"${location}" 
            command_out = command1 + command2 +command3 +command4 
            statout = ( (os.popen(f"{command_out}").read()).strip('\n') )
            
            info.append(statout)
            h = hex(int(statout))
            hexinfo.append(h)
            
        
        
        #or i in range(len(whatInfo)):
         #   print(f"{i} {whatInfo[i]} {info[i]} {hexinfo[i]}")
        self.bottomOfStack = hexinfo[3]
        self.dataStart = hexinfo[4]
        self.dataEnd = hexinfo[5]
        self.heapexpand = hexinfo[6]
        self.argstart = hexinfo[7]
        self.argend = hexinfo[8]
        out = gdb.execute('p $esp', to_string=True)
        m = re.search("0x\w+",out)
        espAddr = m.group(0)
        out = gdb.execute('p $eip', to_string=True)
        m = re.search("0x\w+",out)
        eipAddr = m.group(0)
        hexinfo.append(eipAddr)
        hexinfo.append(espAddr)
        newInfo = []
        for w in whatInfo:
            newInfo.append(w)
        newInfo.append("currentEIP")
        newInfo.append("currentESP")
        #print(self.bottomOfStack,self.dataStart, self.dataEnd, self.heapexpand, self.argstart,self.argend)
        self.statHexInfo = hexinfo 
        self.statWhatInfo = newInfo
        #return whatInfo, hexinfo
        #print(f"info: {info}")
    #print information from that file in a better format so we can read it. 
        print("getThingsFromStatDone")
    def printStatInfo(self):
        print("print stat")
        print( len(self.statWhatInfo),len(self.statHexInfo))
        for i in range(len(self.statHexInfo)):
            print(f"{i} {self.statWhatInfo[i]} {self.statHexInfo[i]}")

    #find the range of the program's stack and heap, if heap is being used. 
    def getStackHeapRangeFromMaps(self):
        PID = isGDBRunningpy()
        if(not PID):
            print("gdb is not running, please run before using this function")
            return
        mapString= os.popen(f'cat /proc/{PID}/maps').read()
        heap_stack_regex = ".+\[heap\]|.+\[stack\]"
        arr = mapString.splitlines()
        heapStart = ""
        heapEnd = ""
        stackStart = ""
        stackEnd = ""
        for line in arr:
            m = re.search(heap_stack_regex,line)
            if(type(m) == re.Match):
                #print(type(m))
                #print(line)
                #avoid problems with grouping nonetype
                try:
                    heapOrStack= m.group(0)
                #    print(f"last chars: {heapOrStack[-3:]}")
                #    print(f"mgroups0: {m.group(0)}")
                    if(heapOrStack[-3:] =="ap]"):
                        #print("this is a heap")
                        heapStart = '0x'+heapOrStack[:8]
                        heapEnd = '0x'+heapOrStack[9:18]
                        #print(f"heapstart: {heapOrStack[:8]}")
                    #   print(f"heapend: {heapOrStack[9:18]}")
                    else:
                        stackStart = '0x'+heapOrStack[:8]
                        stackEnd = '0x'+heapOrStack[9:18]
                    #    print(f"stack: {heapOrStack[:8]}")
                    #    print(f"stackend: {heapOrStack[9:18]}")
                        #print("this is a stack")
                #these contain no errors we're looking for    
                except:
                    pass
        if(not myProgram.window.isVisible()):
            print(f"heap: {heapStart} to {heapEnd}\nstack: {stackStart} to {stackEnd}")
        #return heapStart, heapEnd, stackStart, stackEnd
        self.mapStackBottom = stackEnd
        self.mapStackTop = stackStart
        self.mapHeapBottom = heapEnd
        self.mapHeapTop = heapStart
    def printStackHeapRange(self):
        print(f'heap: {self.mapHeapTop} - {self.mapHeapBottom}')
        print(f'stack: {self.mapStackTop} - {self.mapStackBottom}')
        print(f'fromstat: stackbottom: {self.bottomOfStack}')

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
            self.gdbOutputLayout = QVBoxLayout()
            #self.labelsLayout = QVBoxLayout() 
            self.w1 = self.CodeWindow()
            self.w2 = self.EverythingWindow()
            self.setWindowTitle(f"multiple Windows")
            codeWindowButton = QPushButton("Show/Hide Code Window")
            pprintButton = QPushButton("run pprint")
            pstackButton = QPushButton("print Stack Registers")
            pvarsButton = QPushButton("print variables")
            pfuncButton = QPushButton("print functions")
            gdbNextButton = QPushButton("next")
            pmapButton = QPushButton("Print stack/heap range")
            pstatButton = QPushButton("Print info from /proc/$pid/stat")
            pEverythingButton = QPushButton("Auto run")
            
            pprintButton.clicked.connect((lambda: self.runCommand("pprint")))
            pstackButton.clicked.connect((lambda: self.runCommand("pstack")))
            pvarsButton.clicked.connect((lambda: self.runCommand("pvar")))
            pfuncButton.clicked.connect((lambda: self.runCommand("pfunc")))
            pmapButton.clicked.connect((lambda: self.runCommand("pmap")))
            pstatButton.clicked.connect((lambda: self.runCommand("pstat")))
            gdbNextButton.clicked.connect(self.gdbNext)
            pEverythingButton.clicked.connect(self.printEverything)


            #pvars pfunc pmap pstat pstack 
            #also radio button
            button2 = QPushButton("button 2")
            helpButton =QPushButton("Help")
            self.gdbInput = QLineEdit()
            self.gdbInput.returnPressed.connect(self.gdbInputReturnPressed)
            self.gdbInput.setMaximumWidth(400)

            codeWindowButton.clicked.connect(self.codeWindowButtonClicked)
            button2.clicked.connect(self.buttonTwoClicked)
            helpButton.clicked.connect(self.helpButtonClicked)

            self.centralLabel = QLabel("pprogram output will populate here")
            blanklabel1 = QLabel("")
            blanklabel2 = QLabel("")
            blanklabel3 = QLabel("")
            #add 9 temporary labels to the gird layout
            self.labelsLayout.addWidget(self.centralLabel,0,0)
            self.labelsLayout.addWidget(blanklabel1,0,1)
            self.labelsLayout.addWidget(blanklabel2,0,2)
            self.labelsLayout.addWidget(blanklabel3,0,3)
            for i in range(6):
                testLabel = QLabel(f"")
                testLabel2 = QLabel(f"")
                testLabel3 = QLabel(f"")
                testLabel4 = QLabel(f"")
                self.labelsLayout.addWidget(testLabel,i,0)
                self.labelsLayout.addWidget(testLabel2,i,1)
                self.labelsLayout.addWidget(testLabel3,i,2)
                self.labelsLayout.addWidget(testLabel4,i,3)

            #set the width of the buttons 
            codeWindowButton.setMaximumWidth(200)
            button2.setMaximumWidth(100)
            helpButton.setMaximumWidth(100)

            align = Qt.AlignmentFlag(0) #align left
            
            self.buttonsLayout.addWidget(codeWindowButton,alignment=align)
            
            #codeWindowButton.setMaximumWidth(200)
            
            self.buttonsLayout.addWidget(button2,alignment=align)
            self.buttonsLayout.addWidget(helpButton,alignment=align)
            self.buttonsLayout.addWidget(pprintButton)
            

            self.buttonsLayout2 = QHBoxLayout()
            self.buttonsLayout2.addWidget(pstackButton)
            self.buttonsLayout2.addWidget(pvarsButton)
            self.buttonsLayout2.addWidget(pfuncButton)
            self.buttonsLayout2.addWidget(gdbNextButton)

            self.buttonsLayout3 = QHBoxLayout()
            self.buttonsLayout3.addWidget(pmapButton)
            self.buttonsLayout3.addWidget(pstatButton)
            self.buttonsLayout3.addWidget(pEverythingButton)

            self.checkBoxLayout = QHBoxLayout()
            self.modeCheckBox = QCheckBox("complex")
            self.addRegistersCheckBox = QCheckBox("add registers")
            self.addVarsCheckBox = QCheckBox("add Variables")
            self.addFunctionsCheckBox = QCheckBox("add functions")
            #add pmaps/pstat boxes?
            self.addRegistersCheckBox.toggled.connect(self.itemSelected)
            self.addVarsCheckBox.toggled.connect(self.itemSelected)
            self.addFunctionsCheckBox.toggled.connect(self.itemSelected)
            self.modeCheckBox.clicked.connect(self.modeCheck)

            self.addRegistersCheckBox.setChecked(True)
            self.addVarsCheckBox.setChecked(True)
            self.addFunctionsCheckBox.setChecked(True)

            self.checkBoxLayout.addWidget(self.modeCheckBox)
            self.checkBoxLayout.addWidget(self.addRegistersCheckBox)
            self.checkBoxLayout.addWidget(self.addVarsCheckBox)
            self.checkBoxLayout.addWidget(self.addFunctionsCheckBox)
            
            #self.modeCheckBox.clicked.connect()

            self.commandList = ['pfuncs','pmaps','pprint','pstack','pstat', 'pvars']
            self.outerLayout.addLayout(self.checkBoxLayout)
            self.outerLayout.addLayout(self.buttonsLayout)
            self.outerLayout.addLayout(self.buttonsLayout2)
            self.outerLayout.addLayout(self.buttonsLayout3)
            self.outerLayout.addWidget(self.gdbInput)
            self.testLayout = QVBoxLayout()
            self.testLayout.addLayout(self.labelsLayout)
            #self.outerLayout.addLayout(self.labelsLayout)
            self.outerLayout.addLayout(self.testLayout)
            #i dunno about this one 
            
            self.gdbOutputText = QLabel("output from gdb commands will populate here.")
            self.gdbOutputText.setMaximumWidth(1000)
            self.gdbOutputLayout.addWidget(self.gdbOutputText)
            self.outerLayout.addLayout(self.gdbOutputLayout)
            #self.gdbOutputText.setFixedWidth(500)
            
            
            #self.gdbOutputText.setFixedWidth(10)
            self.widget.setLayout(self.outerLayout)
            #addWidget(widget, fromRow, fromColumn, rowSpan, columnSpan, alignment)
            
            #self.setCentralWidget(widget)
            #generate the help dialogue box, basically will list commands and what they do (pprint docstring more or less)
        def printEverything(self):
            self.w2.populateEverything()
            self.w2.show()
            
        def gdbNext(self):
            gdb.execute('n')
            self.w1.setCodeText()
            self.w1.setNumberLabels()

        #mostly used for dbug    
        def itemSelected(self):
            value = ""
            if self.addRegistersCheckBox.isChecked():
                value=value+"r"
            if self.addVarsCheckBox.isChecked():
                value=value+"v"
            if self.addFunctionsCheckBox.isChecked():
                value=value+"f"    
            #print(value)
            self.optionsSelected = value
            return value      

        def modeCheck(self):
            #print("modecheck first:", self.modeCheckBox.isChecked())
            gdb.execute("pchangemode")
            #print("modecheck after pcm:", self.modeCheckBox.isChecked())
        def runCommand(self, cmd):
            print("executing: ",cmd)
            gdb.execute(cmd) 
            
        def changeCentralLabels(self,text,givenColors=0,givenHeader=0):
            print(f"changing central labels given colors: {givenColors} given headder {givenHeader}")
            tmplist = [""]*len(text[0])
            text.append(tmplist)
            zlist= list(zip(*text))
            #print(zlist)
            #i think this one works. double check math later
            #num_needed=len(text[0])*len(text)
            num_needed=len(text[0])*4
            #print(f"i should need:{num_needed} l-zlist: {len(zlist[0])}")
            if(givenColors):
                print("THIS ONE IS GIVEN COLOR")
                self.setNumLabels(num_needed)
                count = 0
                
                #print(f"i should need:{num_needed} l-zlist: {len(zlist)}")

                #i might need to send this to a function that gets a color for a type of thing
                #basically [0] is a name so that color should test to see if its a function (in the name of functions)
                #etc. though i really dont like that. i can just do this by skipping the 3rd index
                for i in range(len(zlist)):
                    for j in range(len(zlist[i])):
                        if(givenHeader):
                            if(i==0 and j==0):
                                count=count+1
                        if j == 3:
                            pass
                            
                        else:
                            color = zlist[i][3]
                            #change colors to something manageable 
                            if color == 'white':
                                color = 'black'
                            if color == 'yellow':
                                color = '#ff9900'
                            #eg white is never a thing!!!
                            itemWidget = self.labelsLayout.itemAt(count).widget()
                            #itemWidget.setText(f"i: {i} j: {j} {zlist[i][j]}")
                            #itemWidget.setStyleSheet("border: 1px solid black;")
                            
                            outText = f"<html><font color={color}>{zlist[i][j]}</font></html>"
                            #print("~~~~~OUTTEXT~~~~~~~",outText)
                            itemWidget.setText(outText)
                            count=count+1

            else:
                #num_needed=len(text[0])*4
                self.setNumLabels(num_needed)
                count = 0
                
                #print(f"i should need:{num_needed} l-zlist: {len(zlist)}")
                for i in range(len(zlist)):
                    for j in range(len(zlist[i])):
                        if(givenHeader):
                            if(i==0 and j==0):
                                count=count+1
                    
                        itemWidget = self.labelsLayout.itemAt(count).widget()
                        #itemWidget.setText(f"i: {i} j: {j} {zlist[i][j]}")
                        #itemWidget.setStyleSheet("border: 1px solid black;")
                        itemWidget.setText(zlist[i][j])
                        count=count+1    
                        
                    # itemWidget.setText("")
                    # count=count+1
        def setNumLabels(self,num_needed):

            numberCurrentLabels = self.labelsLayout.count()
            print(f"current number of labels: {numberCurrentLabels} number needed: {num_needed}")
            #remove all labels
            for i in reversed(range(numberCurrentLabels)):
                item = self.labelsLayout.itemAt(i)
                item.widget().close()
                self.labelsLayout.removeItem(item)
            #now put back only the ones we need. 
            for i in range(num_needed):
                label = QLabel(f"new label{i}")
                label.setMaximumWidth(200)
                label.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
                
                self.labelsLayout.addWidget(label)        
            
        def gdbInputReturnPressed(self):
            cw = self.w1
            
            
            text = self.gdbInput.text()
            print(text)    
            self.gdbInput.setText("")
            #user definitely ran a command not in this file
            if text =="":
                self.gdbOutputText.setText("please enter a command.")
                return
            if(text[0]!='p'):
                try:
                    out = gdb.execute(text,to_string=True)
                    self.gdbOutputText.setText(out)
                    self.w1.setCodeText()
                    self.w1.setNumberLabels()
                except gdb.error as e:
                    self.gdbOutputText.setText(str(e))
                    self.w1.setCodeText()
                    self.w1.setNumberLabels()    
            else:    
                matches = [match for match in self.commandList if text in match]
                print(matches)
                if(len(matches)>0):
                    self.gdbOutputText.setText("")
                    gdb.execute(text)
                    cw.setCodeText()
                    cw.setNumberLabels()
                    return
                #user ran a gdb command that was not in this program
                else:
                    try:
                        out = gdb.execute(text,to_string=True)
                        self.gdbOutputText.setText(out)
                        self.w1.setCodeText()
                        self.w1.setNumberLabels()
                    except gdb.error as e:
                        self.gdbOutputText.setText(str(e))
                        self.w1.setCodeText()
                        self.w1.setNumberLabels()
                        
                    return
            
           
        def helpButtonClicked(self):
            dlg = self.HelpDialogue()
            dlg.exec()

        def codeWindowButtonClicked(self):
            print("Code Window clicked")
            self.w1.setCodeText()
            self.w1.setNumberLabels()
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
           
        class EverythingWindow(QMainWindow):

            def __init__(self):
                super().__init__()
                self.outerLayout = QVBoxLayout()
                self.widget = QWidget()
                self.widget.setLayout(self.outerLayout)
                self.scroll = QScrollArea()
                #Scroll Area Properties
                self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                self.scroll.setWidgetResizable(True)
                self.scroll.setWidget(self.widget)
                self.setCentralWidget(self.scroll)

        #returns the current line of the program based on the current line  
            def getCodeLine(self):
                currentLine = myProgram.codeWindow.getCurrentLine()
                file_path = myProgram.codeWindow.filepath #myProgram.codeWindow.localfilepath
                
                codeLines = []
                with open(file_path, "r") as f:
                    codeLines = f.readlines()
                print(currentLine)
                print(codeLines, len(codeLines))

                for i in range(len(codeLines)):
                    if i == int(currentLine)-1:
                        print("this line matches", i,currentLine,codeLines[i])
                        return codeLines[i]
                        
            def setAllLabels(self,stuff):
    
                row = 0
                headerCounter = 0
                for singleList in stuff:
                    headder = QHBoxLayout()
                    #currentCodeLine = self.getCodeLine()
                    #add code line number
                    headderLabel = QLabel(f"{self.codelines[headerCounter]}")
                    headderLabel.setStyleSheet("border-top: 2px solid black")
                    headder.addWidget(headderLabel)
                    
                    container = QGridLayout()
                    zlist= list(zip(*singleList))
                    j = 0
                    for thing in zlist:
                        color = thing[2]
                        #if color is meh change it to something good
                        if color == 'white':
                            color = 'black'
                        if color == 'yellow':
                            color = '#ff9900'
                        nameLabel = QLabel(f"<html><font color={color}>{thing[0]}</font></html>")
                        addrLabel = QLabel(f"<html><font color={color}>{thing[1]}</font></html>")
                        dataLabel = QLabel(f"<html><font color={color}>{thing[3]}</font></html>")
                        
                        container.addWidget(nameLabel,row,0)
                        container.addWidget(addrLabel,row,1)
                        container.addWidget(dataLabel,row,2)
                        row = row+1
                    headerCounter = headerCounter+1 
                    self.outerLayout.addLayout(headder)
                    self.outerLayout.addLayout(container)

            def populateEverything(self):
                print("w2 running everything")
                #remove all stacks from the program, so it doesnt mess anything up
                myProgram.trackStacks.clear()
                #delete all breakpoints and get going
                gdb.execute('del breakpoints')
                myProgramFunctions.populateFunctions()
                funcNumbers = myProgramFunctions.functionsLine
                for num in funcNumbers:
                    gdb.execute(f'b {num}')
                i = 0
                gdb.execute('r')
                isRunning = isGDBRunningpy()
                self.codelines = []
                while(isRunning):
                    print("i: ",i)
                    i= i +1
                    try:
                        gdb.execute('pprint everything')
                        self.codelines.append(self.getCodeLine())
                        gdb.execute('n')
                    except gdb.error:
                        break
                        
                    #gdb.execute("pwas automated_all_stacks.txt")
                    isRunning = isGDBRunningpy()
                #print(myProgramFunctions.functionsLine)
                self.setAllLabels(myProgram.trackStacks)
                

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
                
                
                self.getProgramFilePathForWindow()
                self.setWindowTitle(f"{self.localfilepath} Code Window")
                self.layout = QGridLayout() 
                self.label1 = QLabel("")
                self.label2 = QLabel("")  
                self.setCodeText()
                self.setNumberLabels()
                self.layout.addWidget(self.label1,0,0)
                self.layout.addWidget(self.label2,0,1)
            
                widget = QWidget()
                widget.setLayout(self.layout)
                self.setCentralWidget(widget)
                #print(self.label1.text())
                #print(self.label2.text())
            def setCodeText(self):
                s = 'vs'
                with open(self.filepath,'r') as f:
                    code = f.read()
                lexer = CLexer() 
                
                formatter = HtmlFormatter(style=s)
                result = highlight(code, lexer, formatter)
                #print(result)
                css = formatter.get_style_defs()
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
                    
                for line in res3.splitlines():
                    label = QLabel("")
                    label.setText("\n")
                    text2.append(label)
                    #print(line)
                self.label2.setText(res3)
                self.numCodeLines = len(res3.splitlines())
                #self.layout.addWidget(label2,1,1)
                
                #print(t)
                #print(self.label1.text())     
                #print(bst)
            def getBreakpoints(self):
                #print("get breakpoints called")
                breakpointRegex = "\d+$"
                out = gdb.execute('info breakpoints',to_string = True)
                lines = out.splitlines()
                print(out)
                print(lines)
                bps = []
                for line in lines:
                    #print(f"examining {line}")
                    try:
                        #re.findall()
                        m = re.search(breakpointRegex,line)
                    #    print("M is:",m.group(0))
                        bps.append(m.group(0))
                    except:
                        #print('exception in getBreakPoints')
                        pass
                    
                        a = 0
                #print("all breakpoints ", bps)
                uniqueBps = [*set(bps)]
                uniqueBps.sort(key = int)
                #print("unique bps: ",uniqueBps)
                print(f"returning {uniqueBps} from getbreakpoints")
                return uniqueBps

            #there is a delay in this function have to hit enter twice to update things for some reason    
            def setNumberLabels(self):
                print("setting number labels")
                breakpoints = self.getBreakpoints()
            
                bst = ""
                currentLine = self.getCurrentLine()
                #print(type(breakpoints),breakpoints, type(currentLine),currentLine)
                outArr = []
                for i in range(self.numCodeLines):
                    outArr.append(i)
                #print(outArr)    
                for i in range(len(outArr)):
                    innerFound = False
                    for b in breakpoints:
                        
                        if(b == str(i) and str(i)==currentLine):
                            outArr[i] = "ba"
                            innerFound =True
                            break #continue?
                        elif(b == str(i)):
                            outArr[i] = 'b'
                            innerFound =True
                            break
                    if(not innerFound):
                        if(str(i)==currentLine):
                            outArr[i] = "a"
                outst = ""
                for i in range(len(outArr)):
                    if str(outArr[i]) =='ba':
                        outst = outst + "-->B:"+str(i)+"\n"
                        
                    elif str(outArr[i]) == 'a':
                        outst = outst + "-->"+str(i)+"\n"
                        
                    elif str(outArr[i]) == 'b':
                        outst = outst + "B:"+str(i)+"\n"
                        
                    else:
                        outst = outst + str(i)+"\n"
                #print(outst)
                self.label1.setText(outst)
                #self.label1.setText(bst)   
                t = self.label1.text()  

            def getCurrentLine(self):
                if(gdb.selected_inferior().pid):
                    out = gdb.execute("frame",to_string = True)
                    print(out)
                    lines = out.splitlines()
                    
                    try:
                        m = re.search("^\d+", lines[1])
                        numString = m.group(0)#[1:-1]
                        numInt = int(numString)
                    except:
                        numString = 0
                        #this might be fine...?
                        print("error in getCurrentLine")
                        pass
                else:
                    numString = 0   
                #print(f"returning {numString} from getcurrentline") 
                return numString
            def getProgramFilePathForWindow(self):
                line = gdb.execute('info file', to_string = True)
                fpre = "`\/home\/.+'"
                try:
                    m = re.search(fpre,line)
                    self.filepath = m.group(0)[1:-1]
                    self.executable = self.filepath
                    self.filepath = self.filepath+".c"
                except:
                    self.filepath = "unknown.c"
                    self.executable = "unknown"
                    pass
                    
                localfilepath = self.executable
                try:
                    m = re.search("\w+$",localfilepath)
                    localfilepath = m.group(0)
                    
                except:
                    localfilepath = "unknown.c"
                    pass
                if(self.filepath == "unknown.c" or localfilepath == "unknown.c"):
                    print("cannot parse this file, is it named correctly?")  
                    return  
                self.localexecutable = localfilepath
                self.localfilepath = localfilepath+".c"
                print(self.filepath)    



class pwindow (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pwindow,self).__init__("pwindow",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        myProgramWindow.show()
        myProgram.app.exec()
        
pwindow() 

#gdb command that will print stack registers including certain things from info frame and stat/maps
#<<TODO>> add 3rd column of what these things are pointing too 
class pstack (gdb.Command):
    """print the stack registers known at the current point"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pstack,self).__init__("pstack",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        if(isGDBRunningpy()):
            argString = arg.strip('').split('-')
            
            print("invoking pstack")
            print(f"len arg: {len(arg)} it is: {arg} type: {type(arg)} argstring: {argString}")
            myProgramStack.getRegs()
            myProgramStack.sortRegs()
            if(from_tty):
                if(not myProgram.window.isVisible()):
                    
                    myProgramStack.printAll()
                else:
                    pair = myProgramStack.getRegisterPairs()
                    #from pprint how bug
                    #myProgramWindow.changeCentralLabels([myProgramStack.stackRegisterNames,myProgramStack.stackRegisterAddresses,pair])        
            else:
                print("updating gdb window pstack")
                pair = myProgramStack.getRegisterPairs()
                print("before update: ", myProgramStack.stackRegisterNames,myProgramStack.stackRegisterAddresses,pair)
                if(myProgramWindow.isVisible() and argString[0] != 'from_pprint'):
                    myProgramStack.stackRegisterNames.insert(0,"register")
                    myProgramStack.stackRegisterAddresses.insert(0,"address")
                    myProgramWindow.changeCentralLabels([myProgramStack.stackRegisterNames,myProgramStack.stackRegisterAddresses,pair])
                    #myProgramWindow.changeCentralLabels([myProgramStack.stackRegisterNames,myProgramStack.stackRegisterAddresses,pair],1)    
                #pair.insert(0,"pointed to")
                #print(myProgramVariables.variableInfo)
                
                #same bug figure out how to invoke from pprint and the window seperately 
                
                #gdbWindow.updateGDBLabelText([myProgramStack.stackRegisterNames,myProgramStack.stackRegisterAddresses,pair])    
            # if window.isVisible():   
            #     myProgramStack.printAll()
        else:
            print("not debugging, please run before using.")
        
pstack() 

class pfunc (gdb.Command):
    """print the functions known to the program at the current point"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pfunc,self).__init__("pfunc",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        argString = arg.strip('').split('-')
        #print(arg)
        
        
        print(f"invoking pfunc {arg} from_tty: {from_tty} isVisible: {myProgramWindow.isVisible()}")    
        myProgramFunctions.populateFunctions()
        print("myproginfo: ",myProgramFunctions.funcInfo)
        #myProgramFunctions.functionsName
        #myProgramFunctions.fun
        if(from_tty):
            myProgramFunctions.printAll()

            
        #justification is not easy. punt for later its a small issue. 
        if(myProgramWindow.isVisible()):
            myProgramFunctions.funcSortByNumber()

            names = myProgramFunctions.functionsName 
            addrs = myProgramFunctions.functionsAddr
            nums = myProgramFunctions.functionsLine
            blank = [""]*len(names)
            #nameout = []
            #a_list = [[1,2], [2,3], [3,4]]
            #b_list = [[9], [10,11], [12,13]]
            new_list = [a +':'+ b for a, b in zip(nums, names)]
            
            argString = arg.strip('').split('-')
            if(myProgramWindow.isVisible() and argString[0] != 'from_pprint'):
                new_list.insert(0,"line:function")
                addrs.insert(0,"address")
                blank.append("")
                myProgramWindow.changeCentralLabels([new_list,addrs,blank])
            #myProgramWindow.changeCentralLabels([new_list,addrs,blank])   
             
            # myProgramFunctions.funcSortByNumber()
            # outst=myProgramFunctions.printAll()
            # printme = []
            # for o in outst:
            #     #printme.append(o)
            #     print(o)
            # print("outst[i]~~~~")
            # for i in range(len(outst)):
            #     print(i,outst[i][1])    
            #myProgramWindow.setNumLabels(2) 
            
            #myProgramWindow.centralLabel.setText(printme)
            #print(printme)

pfunc()

#redirects pfuncs to pfunc in case of typo.
#this would cause confusion, so just forward it to pfunc
class pfuncs (gdb.Command):
    """calls pfunc"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pfuncs,self).__init__("pfuncs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        argString = arg.strip('').split('-')
        print(f"invoking pfuncs {arg}") 
        gdb.execute(f'pfunc {arg}')  
pfuncs()

#####~~~~~MAIN~~~~~#####
#declare objects so this file can start collecting information
#define like this for ease of use later
# global myProgram
myProgram = Program()
myProgramStack = myProgram.programStack
myProgramHeap = myProgram.programHeap
myProgramFunctions = myProgram.programFuncs
myProgramVariables = myProgram.programVariables
myProgramWindow = myProgram.window
print("Welcome to PPGDB Alpha build.")
print("Please ensure that the executable and filename are in the same folder as ppgdb.py and they share their name. EG: myExecutable and myExecutable.c")
print("The program has started debugging and a breakpoint has been set in main.")
print("For help please use \"help pprint\"")
print("to launch the GUI please use the command \"pwindow\"")



class resource (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        gdb.execute("source test.py")
resource() 
#app.setStyleSheet(css)

# gdbWindow = myProgramWindow.gdbWindow
# gdbWindow.getBreakpoints()

#this method prints things nicely. 
def printPair(names,addrs,colors,data):
    print("invoking printpair")
    const = 20
    print("---------------------------")
    print("reg/var/func/info    address       what is stored <what is pointing to?>")
    print("---------------------------")
    for i in range(len(names)):
        #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
        nameSize = len(names[i])
        spaceString = " "
        for j in range(const-(nameSize)):
            spaceString = spaceString + " "
        if(data == ""):
            if (names[i]== 'saved_eip' or names[i]=='previous_sp'):
                out = colored(f"{names[i]}{spaceString}{addrs[i]}",colors[i], attrs=['bold'])
            else:
                out = colored(f"{names[i]}{spaceString}{addrs[i]}",colors[i])
        else:
            out = colored(f"{names[i]}{spaceString}{addrs[i]}     {data[i]}",colors[i])
        print(out)

#gdb command to print information from the stat file. 
class pstat (gdb.Command):
    """print information from proc/$pid/stat"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pstat,self).__init__("pstat",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        #current project make this flow better. 
        print("invoking pstat")
        myProgram.getThingsFromStat()
        #from tty is user terminal
        if(from_tty and not myProgramWindow.isVisible()):
            #print("from tty true and not visible returning")
            myProgram.printStatInfo()
            return
        #if myProgramWindow.isVisible():    
        
        #sort the list by address
        for i in range(len(myProgram.statHexInfo)):
            for j in range(len(myProgram.statHexInfo)):
                if int(myProgram.statHexInfo[i],16) < int(myProgram.statHexInfo[j],16):
                    #print("is true")
                    tmpaddr = myProgram.statHexInfo[i]
                    myProgram.statHexInfo[i] = myProgram.statHexInfo[j]
                    myProgram.statHexInfo[j] = tmpaddr
                    tmpname = myProgram.statWhatInfo[i]
                    myProgram.statWhatInfo[i] = myProgram.statWhatInfo[j]
                    myProgram.statWhatInfo[j] = tmpname            
        
        
        argString = arg.strip('').split('-')
        if(myProgramWindow.isVisible() and argString[0] != 'from_pprint'):
            #print("window is visibable and its not from pprint")
            myProgram.statWhatInfo.insert(0,"info") 
            myProgram.statHexInfo.insert(0,"address")  
            
        #add the 2 lists to the gui
            count = 0
            if(1):
                myProgramWindow.setNumLabels(len(myProgram.statWhatInfo)*4)
                for i in range(len(myProgram.statWhatInfo)):
                    for j in range(4):
                        if j ==0:
                            
                            nameWidget = myProgramWindow.labelsLayout.itemAt(count).widget()
                            nameWidget.setText(myProgram.statWhatInfo[i])
                            
                        elif j ==1:
                            
                            addrWidget = myProgramWindow.labelsLayout.itemAt(count).widget()
                            addrWidget.setText(myProgram.statHexInfo[i])    
                            
                        else:    
                            
                            blankWidget = myProgramWindow.labelsLayout.itemAt(count).widget()
                            blankWidget.setText("")        
                        
                        count=count+1
        
        # for w in myProgram.statWhatInfo:
        #     print(w)
           
        
pstat() 

#gdb command to print information from the maps file 
class pmaps (gdb.Command):
    """print informtaion from proc/$pid/maps"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pmaps,self).__init__("pmaps",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        argString = arg.strip('').split('-')
        if(not myProgram.window.isVisible()):
            print("invoking pmaps")
            myProgram.getStackHeapRangeFromMaps()    
        else:
            myProgram.getStackHeapRangeFromMaps()

            h = f'heap: {myProgram.mapHeapTop } - {myProgram.mapHeapBottom}\n'
            s = f'stack: {myProgram.mapStackTop } - {myProgram.mapStackBottom }\n'
            
            if(myProgramWindow.isVisible() and argString[0] != 'from_pprint'):
                myProgramWindow.setNumLabels(4)
                myProgramWindow.labelsLayout.itemAt(0).widget().setMaximumWidth(500)
                #part visual bug here <<RET TODO>>
                myProgramWindow.labelsLayout.itemAt(0).widget().setText(h+s)
            

        if(from_tty):
            myProgram.printStackHeapRange()
        
pmaps() 
#<<TODO>> make saved_EIP point to eip register as data 
#<<rethere pprint>>
class pprint (gdb.Command):
    """run all p commands and hope for the best
    <copy paste information for all functions here>  gdb.execute('pfunc')
    To open gui mode the command is 'pwi' or 'pwindow'
    supported commands:
        'pvars'
            Prints variables, their contents, and location on the stack
    
        'pfunc'
            Prints functions and their location on the stack
            
        'pmap'
            Prints information from /proc/$PID/maps

        'pstat' 
            Prints information from /proc/$PID/stat

        'pstack'
            prints contents of the stack at the current line in the program. 
            
        'pprint'
            print all stack information and display with the current mode 
                default mode: 
                    print all simple information. certain information from /proc/$pid/stat and /maps has been left out for simplicity.
                complex mode:
                    print everything, Yes Everything.
                [not implamented]    
                    <Debug mode>: print debug information (lots of terminal output helpful trace information in finding problems with the program )
        'pauto'
            Prints stack information for each line in the code reachable by gdb "n"
                displays this information in the created file "all_stacks.txt" 
        'pas'
            print all stacks
                print stack information for each time pprint was called.         
        [not implamented at this time]  
        'pchangecolor' type color
            type: var, func, special, regs
                var: changes variable color (default: << color here >>)
                func: changes functions colors (default: << color here >>)
                reg: changes general register colors (default: << color here >>)
                special: changes the special registers colors ('eip', 'edx', 'edi', 'saved_ebp')
            supported colors: https://pypi.org/project/termcolor/

            
    """
    def __init__(self):
                                 #cmd user types in goeshere
        super(pprint,self).__init__("pprint",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        #need flag for all, gui, ...tui?
        # if(myProgram.mode =='complex'):
        #     builderPrint()
        #     return
        #need add extranious things like data and stuff
        bigListNames = []
        bigListAddrs = []
        bigListColors = []
        bigListData = []
        #argString = arg.strip('').split('-')
        
        print("invoking pprint")
        gdb.execute('pfunc from_pprint')
        gdb.execute('pvars from_pprint')
        print("pvars done")
        gdb.execute('pmap from_pprint')
        print('pmap done')
        gdb.execute('pstat from_pprint')
        print("pstat done")
        gdb.execute('pstack from_pprint')
        print("p stack done")
        myProgramStack.getFrameInfo()
        
        print("gathered all data ")
        #manual stuff 
        #map 
        #may need to check if empty here 
        # if(myProgram.mapHeapBottom==''):
        #     pass
        # else:
        if(myProgram.mapHeapBottom == ""):
            pass
        else:
            bigListNames.append("map_heap_bottom")
            bigListAddrs.append(myProgram.mapHeapBottom)
            bigListNames.append("map_heap_top")
            bigListAddrs.append(myProgram.mapHeapTop)
            bigListColors.append("white")
            bigListColors.append("white")

        bigListNames.append("map_stack_bottom")
        bigListAddrs.append(myProgram.mapStackBottom)
        bigListNames.append("map_stack_top")
        bigListAddrs.append(myProgram.mapStackTop)
        bigListColors.append(myProgramStack.boundryColor)
        bigListColors.append(myProgramStack.boundryColor)
        if(not myProgram.window.isVisible()):
            print("finished appending mapstack")
        #automated stuff 
        #stack registers
        #stack registers is not apending the color properly when changing
        if myProgramWindow.addRegistersCheckBox.isChecked() or not myProgramWindow.isVisible():
            special_registers = ['eip', 'edx', 'edi', 'saved_ebp'] #double check these 
            for i in range(len(myProgramStack.stackRegisterNames)):
                bigListNames.append(myProgramStack.stackRegisterNames[i])
                bigListAddrs.append(myProgramStack.stackRegisterAddresses[i])
                found = 0
                for specReg in special_registers:
                    
                    if(myProgramStack.stackRegisterNames[i] == specReg):
                        bigListColors.append(myProgram.specialRegisterColor)
                        found = 1
                if(not found):    
                    bigListColors.append(myProgram.regColor)
        if(not myProgram.window.isVisible()):        
            print("appended stack registers")    

        #functions
        if myProgramWindow.addFunctionsCheckBox.isChecked() or not myProgramWindow.isVisible():
            for i in range(len(myProgramFunctions.functionsName)):
                bigListNames.append(myProgramFunctions.functionsName[i])
                bigListAddrs.append(myProgramFunctions.functionsAddr[i])
                bigListColors.append(myProgram.funcColor)
        if(not myProgram.window.isVisible()):
            print("appended functions")        
        #variable info
        if myProgramWindow.addVarsCheckBox.isChecked() or not myProgramWindow.isVisible():
            for i in range(len(myProgramVariables.varNames)):
                bigListNames.append(myProgramVariables.varNames[i])
                bigListAddrs.append(myProgramVariables.varAddrs[i])
                bigListColors.append(myProgram.varColor)
             
        #stat 
        if(myProgram.mode != "default" or myProgramWindow.modeCheckBox.isChecked()):# or myProgram.mode != "simple"):
            for i in range(len(myProgram.statHexInfo)):
                bigListNames.append(myProgram.statWhatInfo[i])
                bigListAddrs.append(myProgram.statHexInfo[i])
                bigListColors.append("white")
        for name in bigListNames:
            try:
                #variable type with whatis
                #out = gdb.execute(f"whatis {var}",to_string = True)
                #self.getVariableType()
                #print(f"{var}: {out}")
                out = gdb.execute(f"print {name}",to_string = True)
                o = out.split()
                #o = o.replace("'",'')
                #print(f"{var}: {out} o:{o} len: {len(o)}")
                if(len(o)>3):
                    #remove ' and " characters
                    d1 = o[3].strip('\"')
                    datast =d1.replace("'",'')
                    #print("this is a character")
                #   print(print(f"{var}: {o[3][0]}"))
                else:
                    #remove ' and " characters
                    d1 = o[2].strip('\"')
                    datast =d1.replace("'",'')
            #dont add data that has has not been initialized yet. 
                #print(f"datast: {datast}")
                if(not myProgram.window.isVisible()):
                    print("datast: ", datast)
                if(datast=='<error:'):
                   bigListData.append('null') 
                elif(datast=='()}' or datast=='(int)}' or datast=='(int,'):
                   bigListData.append('function')       
                #print(f"the datast for {var}: {datast} 0th_char: {datast[0]}")  
                elif(datast==''):
                    bigListData.append('')
                else: 
                    bigListData.append(datast)
            #except gdb.MemoryError or gdb.error:
            except:
                #print("some memerror, ignoring")
                bigListData.append('')
            
            boundryList = ["esp", "saved_ebp", "previous_sp"]
        for i in range(len(bigListNames)):
            for b in boundryList:
                if (bigListNames[i] == b ):
                    bigListColors[i] = myProgramStack.boundryColor 
        for i in range(len(bigListNames)):
            if (bigListNames[i] == "argv" ):
                bigListColors[i] = myProgram.varColor 
        for i in range(len(bigListNames)):
            if (bigListNames[i] == "esp" ):
                bigListData[i] = "$sp"
        
        for i in range(len(bigListNames)):
         #   print(f"bigdata: {i}  {bigListData[i]}")
        #print(len(bigListData))     
            if (bigListNames[i] == 'saved_ebx'):
                bigListColors[i] = 'white'       
                for j in range(len(bigListData)):
                    if(bigListNames[j] == 'ebx'):
                        bigListData[i] = 'ebx_'+bigListAddrs[j]
                        bigListData[j] = 'saved_ebx_'+bigListAddrs[i]
                        if(not myProgram.window.isVisible()):
                            print("eip has been found")
                        break

            if (bigListNames[i] == 'saved_eip'):
                bigListColors[i] = 'magenta' 
                  
                for j in range(len(bigListData)):
                    if(bigListNames[j] == 'eip'):
                        bigListData[i] = 'eip_'+bigListAddrs[j]
                        if(not myProgram.window.isVisible()):
                            print("eip has been found")
                        break
            if( bigListNames[i] == 'previous_sp'  ):
                bigListColors[i] = 'magenta'   
                out = gdb.execute('p $sp',to_string = True)
                try:
                    m = re.search('0x\w+',out)
                    spAddr = m.group(0)
                    bigListData[i] = "$sp_"+spAddr
                except:
                    pass

        if(from_tty):
            if(not myProgram.window.isVisible()):
                printPair(bigListNames,bigListAddrs,bigListColors,bigListData)
          
        sortedNames, sortedAddrs, sortedColors, sortedData = sortTheBigList(bigListNames,bigListAddrs,bigListColors,bigListData)
        if(myProgram.window.isVisible() and not arg == "everything"):
            
            #printPairNoColor(bigListNames,bigListAddrs,bigListData)
            #myProgram.window.changeCentralLabels([bigListNames,bigListAddrs,bigListData])
            myProgram.window.changeCentralLabels([sortedNames,sortedAddrs,sortedData,sortedColors],1)
       
            #print(sortedNames,sortedAddrs,sortedData)
           # print(bigListNames,bigListAddrs,bigListData)
        #myProgram.window.gdbWindow.updateGDBLabelText([sortedNames,sortedAddrs,sortedColors,sortedData],1)
            #<<TODO>>
            #the window is visible here, so lets display the contents there
            #<<rethere>>
            #printPair(bigListNames,bigListAddrs,bigListColors,bigListData)  
        #short message about what color things are 
        varout = colored("variables "+myProgram.varColor,myProgram.varColor)
        funcout= colored("functions "+myProgram.funcColor,myProgram.funcColor) 
        regsout = colored("regs " + myProgram.regColor, myProgram.regColor)
        specregsout = colored("special registers " + myProgram.specialRegisterColor, myProgram.specialRegisterColor)
        stackboundry = colored("stack boundry "+myProgramStack.boundryColor, myProgramStack.boundryColor)
        if(not myProgram.window.isVisible()):
            print(varout,funcout,regsout, specregsout, stackboundry)
        #now print the full thing 
        if(from_tty):
            if(not myProgram.window.isVisible()):
                printPair(sortedNames,sortedAddrs,sortedColors,sortedData)
        
        myProgram.sortedAddrs = sortedAddrs
        myProgram.sortedNames = sortedNames
        myProgram.sortedColors = sortedColors
        myProgram.sortedData = sortedData
       # print(len(sortedAddrs), len(sortedNames), len(sortedColors))
        #only append if there has been changes
        #we also dont care about the list being "unhashable" after the first time we call pprint anyway
        try:
            if(set(myProgram.trackStacks) == set()):
                #myProgram.addStackTrack(sortedNames,sortedAddrs,sortedData,sortedColors)
                
                myProgram.trackStacks.append([sortedNames,sortedAddrs,sortedColors,sortedData])
        except:
            pass
        localSet = set(sortedAddrs)
        #print("local set: ",localSet)
        #print("myprogramstacks ", myProgram.trackStacks)
        for s in myProgram.trackStacks:
            #print(s)
            trackedSet = set(s[1])
            
            print("set difference: ", localSet - trackedSet)
            print("len of labels:", len(sortedNames))
            #change to != later <<TODO>>
            if(trackedSet - localSet == set()):
                if(not myProgram.window.isVisible()):
                    print("nothing to do here the set is empty")
                #print(trackedSet)
            else:
                if(not myProgram.window.isVisible()):
                    print("not empty add to list")
                
                myProgram.trackStacks.append([sortedNames,sortedAddrs,sortedColors,sortedData])
                break
        # localStackLine = n2
        # for line in myProgram.trackStackLines:
        #     if line == localStackLine:
        #         return      
        # myProgram.trackStackLines.append(localStackLine) 
        # myProgram.trackStacks.append([sortedNames,sortedAddrs,sortedData,sortedColors])
        #myProgram.addSorted(sortedAddrs,sortedNames,sortedColors)
        
pprint() 

def printPairNoColor(names,addrs,data):
    print("print pair no color invoked")
    const = 20
    print("---------------------------")
    print("reg/var/func/info    address       what is stored")
    print("---------------------------")
    for i in range(len(names)):
        #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
        nameSize = len(names[i])
        spaceString = " "
        for j in range(const-(nameSize)):
            spaceString = spaceString + " "
        if(data == ""):
            if (names[i]== 'saved_eip' or names[i]=='previous_sp'):
                out = names[i]+spaceString+addrs[i]
            else:
                out = names[i]+spaceString+addrs[i]
        else:
            out = names[i]+spaceString+addrs[i]+"     "+data[i]
        print(out)

#sorts the big list of the stack/heap/registers, basically whatever you give it .
#if effeciency becomes a concern, revisit this function and use a better sorting alg. 
#Merge Sort is one that is tempting to use based on the nature of this program. 
def sortTheBigList(reglist, regaddrs,colors, data):
    #regaddrs = self.registerAddresses 
    #reglist = self.registerNames
    
    #dont bother sorting if the length is only 1. 
    #does it even count as an optimization 
    # if its only ever called once?
    if(len(regaddrs)==1):
        pass
    else:
        
        for i in range(len(regaddrs)):
            for j in range(len(regaddrs)):
                # < should be the correct direction
                if int(regaddrs[i],16) < int(regaddrs[j],16):
                # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                    tmpaddrs = regaddrs[i]
                    regaddrs[i] = regaddrs[j]
                    regaddrs[j] = tmpaddrs
                    templist = reglist[i]
                    reglist[i] = reglist[j]
                    reglist[j] = templist
                    tmpcolor = colors[i] 
                    colors[i] = colors[j]
                    colors[j] = tmpcolor
                    tmpdata = data[i]
                    data[i] = data[j]
                    data[j] = tmpdata
    return reglist, regaddrs, colors, data
def isGDBRunningpy():
        pid =  (gdb.selected_inferior().pid)
        if(pid<=0):
            print("i am not running")
            return 0
        else:
            if(not myProgram.window.isVisible()):
                print(f"i am running, my pid is: {pid}")
            return pid

class pAllStacks (gdb.Command):
    """print all stack information collected so far with pprint
    supported args (number of stacks to print) <<TODO>>
    color updates only reflect from the point done forward, does not affect previous stack colors
    eg if variables are white on stack 1 but changed after pprint is called this change will only 
    be reflected from stack 2 onwards"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pAllStacks,self).__init__("pas",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        if len(arg)>0:
            print(f"arg invoke: {arg}")
        print("invoking print all stacks") 
        print(f"from_tty: {from_tty}")
        print(f"len arg: {len(arg)}")
        s = myProgram.trackStacks
        i = 0
        if(from_tty or arg == "-c"):
            for stack in s:
                print(f"~~~~stack number {i}~~~~")
                i= i +1
                #printPair(names,addrs,colors,data):
                printPair(stack[0],stack[1],stack[2],stack[3])
        else:
            for stack in s:
                print(f"~~~~stack number {i}~~~~")
                i= i +1
                printPairNoColor(stack[0],stack[1],stack[3])
        #print(f"fromtty: {from_tty} arg: {arg}")        
pAllStacks()

#modify the printpair cmd to do more than one per columns 
class writeStacksToFile (gdb.Command):
    """print all stack information collected so far with pprint
    supported args (number of stacks to print) <<TODO>>
    color updates only reflect from the point done forward, does not affect previous stack colors
    eg if variables are white on stack 1 but changed after pprint is called this change will only 
    be reflected from stack 2 onwards"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(writeStacksToFile,self).__init__("pwas",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking writeStacksToFile")
        if(len(arg)>0):
            filename = arg
        else:
            filename = "all_stacks.txt"
        out = gdb.execute('pas',to_string = True)
        lines = out.splitlines()
        with open(filename,'w') as f:
            for line in lines:
                print(line)
                f.write(line)
                f.write("\n")
          
writeStacksToFile()


#modify the printpair cmd to do more than one per columns 
#<<rethere>> <<TODO>>
class pAutomatedTest (gdb.Command):
    """automatically run each line of the file, collect stack information, and print to file """
    def __init__(self):
                                 #cmd user types in goeshere
        super(pAutomatedTest,self).__init__("pauto",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking pAutomatedTest")
        
        myProgramFunctions.populateFunctions()
        funcNumbers = myProgramFunctions.functionsLine
        for num in funcNumbers:
            gdb.execute(f'b {num}')
        i = 0
        isRunning = isGDBRunningpy()
        while(isRunning):
            print("i: ",i)
            i= i +1
            try:
                gdb.execute('pprint')
                gdb.execute('n')
            except gdb.error:
                break
                
            #gdb.execute("pwas automated_all_stacks.txt")
            isRunning = isGDBRunningpy()
        #print(myProgramFunctions.functionsLine)
        if(len(arg)>0):
            if(arg == "-t"):
                gdb.execute('pas -c')
        else:        
            gdb.execute('pwas')
         
pAutomatedTest()

class changemode (gdb.Command):
    """change the current program mode
    simple/default: 
        print most important inforomation leaving out <certain things>
        when pchangemode is called witn no arguments or with "default," "simple"
    verbose/complex: 
        print everything. yes, everything. 
    builder: 
        build print output only displaying things user wants
            example: registers and variables but not functions and boundry information
                pregs, pvars, pprint"""
                
    def __init__(self):
                                 #cmd user types in goeshere
        super(changemode,self).__init__("pchangemode",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        print("invoking changemode") 
        if myProgram.mode == 'default':
            myProgram.mode = 'complex'
            myProgramWindow.modeCheckBox.setChecked(True)
        elif myProgram.mode == 'complex':
            myProgram.mode = 'default'
            myProgramWindow.modeCheckBox.setChecked(False)
        else: 
            print("invalid change somehow check pchangemode\nChanging to default.")    
            myProgram.mode = "default"
        # if(len(arg))<1:
        #     myProgram.mode = 'default'
        #     print("changed mode to default")    
        # print(f"from_tty: {from_tty}")
        # print(f"len arg: {len(arg)} args: {arg}")
        # myProgram.mode = arg

changemode()

class tcmd (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("tcmd",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        #gdb.execute("source test.py")
        print("test print completed")
resource() 


            #if obj.__class__ == pqt6:
                #print("something pyqt6")
            #print(name)


# #this MUST be the very last thing in this file

# import inspect
# def getAllClasses():
#     classList = []
#     for name, obj in inspect.getmembers(sys.modules[__name__]):
#             if inspect.isclass(obj):
#                 if name[0] != 'Q' and name[0:4] != 'pyqt':
#                     print(name)
#                     classList.append(name)            
#     return classList              
# getAllClasses()    