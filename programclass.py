#start conventionalizing
#NAME GOES FIRST THEN ADDRESS 
###########todo 
# """docstrings""" (ie help <functioname>)
# get/print everything 
# send it to GUI for nice picture (prototype is built in windowonly.py)
#need to build a "tracking" command
#or just auto do this x times and save a picture of the stack each time
#add mode support 
#more doc string stuff 
#prettyify output 
#sperate out modes and how they work 
#color 
# builder mode (most complicated)
# simple mode (probably default)
# complex mode (just print everything basically done)
#import statements for gui (pyqt6 etc) should ONLY be in that function (hopefully so people that dont want/need to use gui dont need to install pyqt6)
#display things that have data
#have a visual toggle siwtch between gui and text maybe a prompt like "would you like to enable visual mode?"
#i dont know why there is a difference between what is reported in stat and map
#ESP is the stack pointer for the system stack, changes when data is pushed or popped from stack 
#ebp is points to the base
#General registers
# EAX EBX ECX EDX
# Segment registers
# CS DS ES FS GS SS
# Index and pointers
# ESI EDI EBP EIP ESP
# Indicator
# EFLAGS






import re
import os


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
        print("printing stack")
        for s in self.heapBoth:
            print(s)
        self.sortRegs()
        print("sorted stack")
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
        
        self.stackRegisterAddresses.append(regAddress)
        self.stackRegisterNames.append(regName)
        self.stackInit = 1
        self.both.clear()
        self.both = [self.stackRegisterNames,self.stackRegisterAddresses]

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
        print("printing stack")
        regColors =['white'] * len(self.stackRegisterAddresses)        
        printPair(self.stackRegisterNames,self.stackRegisterAddresses,regColors, "")
        # self.printPretty()
        # self.sortRegs()
        # print("sorted stack")
        # self.printPretty()
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
        print("passed exception")
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
        
        if(1):
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
            print(f"adding: {reg}")
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
        print('before printRegisters')
        printRegisters(frameRegNames,frameRegs)
        print("after printRegisters")
        # for i in range(len(frameRegNames)):
        #     print(f"{i} {frameRegNames[i]} {frameRegs[i]}")
        #     self.addReg(frameRegNames[i],frameRegs[i])
        return frameRegNames, frameRegs
    
#function that reloads this file into gdb with any changes. 
# is not useful unless editing this file directly.     
class resource (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("source programclass.py")
resource() 

#basically just runs show commands but as wc which is easy and lazy. 
class whatCommands (gdb.Command):
    """shows the command history the user has entered so far"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(whatCommands,self).__init__("wc",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("show commands")

whatCommands()

#class of the functions inside a program, for example main
class Func:

    def __init__(self):
        #containers 
        self.functionsName = []
        self.functionsLine = []
        self.functionsAddr = []
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]

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
        for i in range(len(names)):
            #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
            nameSize = len(names[i])
            numberSize = len(nums[i])
            spaceString = " "
            for j in range(const-(nameSize+numberSize)):
                spaceString = spaceString + " "
            print(f"{nums[i]}:{names[i]}{spaceString}{addrs[i]}")
    
#primary way to keep track of things


 #command to set colors for different things 

#bug in changing registers (problem, yes)
class changeColor (gdb.Command):
    """schanges the color of certain information. 
    invoke: pcc
    things that can be changed:
    registers (reg)
    variables (var)
    functions (func)

    supported colors: 
        grey red green yellow blue magenta cyan white
        """
    def __init__(self):
                                 #cmd user types in goeshere
        super(changeColor,self).__init__("pcc",gdb.COMMAND_USER)
        
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking changeColor")
        print(f"args: {arg}")
        argst = arg.split()
        print(f"split: {argst}")
        #change back to default
        #if(len(arg==0)):
        #myProgram.changeColor('red','nope')
        #try: except: IndexError
        try:
            myProgram.changeColor(argst[1],argst[0])
        except IndexError:
            print("invalid number of arguments. supported call: pcc <type> <color>")
changeColor()
 # command to check valid mode    

#the primary class of this program. 
#the program class is the premary mechanism for storing, retrieving, and interacting with the various parts of the running program. 
class Program:

    def __init__(self):   
        #programs have a stack, a heap, functions, and variables.
        self.programStack = Stack()
        self.programHeap = Heap()
        self.programFuncs = Func()
        self.programVariables = Variables()

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
        self.executable =""
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
        self.getProgramFilePath()
        self.sortedAddrs = [] 
        self.sortedNames = []
        self.sortedColors = []
    def addSorted(self, ssortedAddrs, ssortedNames, sortedColors):
        print(f"insorted: {ssortedAddrs}")
        for a in ssortedAddrs:
        
            self.sortedAddrs.append(a)
        for n in ssortedNames:
            self.sortedNames.append(n)
        self.sortedColors = sortedcolors
  
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
        out = gdb.execute("info line",to_string = True)
        fileregex = "\".+\""
        m = re.search(fileregex,out)
        filename = m.group(0).strip("\"" )
        #print(filename)
        #print(filename[0:-2])
        self.filepath = filename
        self.executable = filename[0:-2]
    #get the running program's process ID
    #this starts debugging leaving it on the first line of main. 
    def getPID(self):
        gdb.execute('b main')
        gdb.execute('r')
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
        useful_stack_info = [23,26,27,28,29,30,45,46,47,48,49,50,51,52]
        whatInfo = ["vsize","startcode","endcode", "startStack", "currentESP", "currentEIP", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"]
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
        self.dataStart = hexinfo[6]
        self.dataEnd = hexinfo[7]
        self.heapexpand = hexinfo[8]
        self.argstart = hexinfo[9]
        self.argend = hexinfo[10]
        
        #print(self.bottomOfStack,self.dataStart, self.dataEnd, self.heapexpand, self.argstart,self.argend)
        self.statHexInfo = hexinfo 
        self.statWhatInfo = whatInfo
        #return whatInfo, hexinfo
        #print(f"info: {info}")
    #print information from that file in a better format so we can read it. 
    def printStatInfo(self):
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
#variables of a program
class Variables:
    def __init__(self):  
        #containers
        self.varNames = []
        self.varAddrs = []
        self.varDatas = []
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
                if(len(o)>3):
                    #remove ' and " characters
                    d1 = o[3].strip('\"')
                    datast =d1.replace("'",'')
                    print("this is a character")
                 #   print(print(f"{var}: {o[3][0]}"))
                else:
                    #remove ' and " characters
                    d1 = o[2].strip('\"')
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
            print("invoking pvars")
            myProgramVariables.getLocalVariables()
            if(from_tty):
                myProgramVariables.printAll()
            #myProgramVariables.sort()
            #myProgramVariables.printAll()
        else:
            print("not debugging, please run before using.")
pvars() 
class pglobalvars (gdb.Command):
    """find and print the variables known at the current point"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pglobalvars,self).__init__("pgv",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        myProgramVariables.getLocalVariables()
pglobalvars() 

#<<TODO>>
#invoke the printALl method regardless of what is passed in. 
def printObject(obj):
    obj.printAll()

#gdb command to print information from the stat file. 
class pstat (gdb.Command):
    """print information from proc/$pid/stat"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pstat,self).__init__("pstat",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking pstat")
        myProgram.getThingsFromStat()
        if(from_tty):
            myProgram.printStatInfo()
pstat() 

#gdb command to print information from the maps file 
class pmaps (gdb.Command):
    """print informtaion from proc/$pid/maps"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pmaps,self).__init__("pmaps",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking pmaps")
        myProgram.getStackHeapRangeFromMaps()
        if(from_tty):
            myProgram.printStackHeapRange()
        
pmaps() 

#<<TODO>>?
class pprogram (gdb.Command):
    """the big print program, need more docstring"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pprogram,self).__init__("pprogram",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking pprogram")
        # print(vars(myProgram))
        # print(vars(myProgramStack))
        # print(vars(myProgramFunctions))
        # print(vars(myProgramVariables))
        print(myProgram.PID)
        print((gdb.selected_inferior()))
pprogram() 


#find out of gdb is running a current program or not 
#not really used <<TODO>>
class isGDBRunning (gdb.Command):
    """figure out if gdb is running or not"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(isGDBRunning,self).__init__("amirunning",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        pid =  (gdb.selected_inferior().pid)
        if(pid<=0):
            print("i am not running")
            return 0
        else:
            print(f"i am running, my pid is: {pid}")
            return 1
isGDBRunning()
class pinfoframe (gdb.Command):
    """figure out if gdb is running or not"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pinfoframe,self).__init__("pif",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking pinfoframe")
        myProgramStack.getFrameInfo()
pinfoframe()

#function that determines if GDB is running an inferior program (is it currently running a program)
def isGDBRunningpy():
        pid =  (gdb.selected_inferior().pid)
        if(pid<=0):
            print("i am not running")
            return 0
        else:
            print(f"i am running, my pid is: {pid}")
            return pid


#####~~~~~MAIN~~~~~#####
#declare objects so this file can start collecting information
#define like this for ease of use later
myProgram = Program()
myProgramStack = myProgram.programStack
myProgramHeap = myProgram.programHeap
myProgramFunctions = myProgram.programFuncs
myProgramVariables = myProgram.programVariables

#print welcome message
print("welcome to PPGDB")
print("the executable is currently running and a breakpoint has been set in main.")
print("all program modules begin with the letter p.")
print("to see available modules use \"help pprint\"")

#myProgramStack.getFrameInfo()
#printObject(myProgramStack)

#RET TESTING
# theap = Heap()
# theap.addReg('reg1','0xfffffff1')
# theap.addReg('reg4','0xfffffff4')
# theap.addReg('reg2','0xfffffff2')
# theap.printAll()
# tstack = Stack()
# tstack.addReg('reg1','0xfffffff1')
# tstack.addReg('reg4','0xfffffff4')
# tstack.addReg('reg2','0xfffffff2')
# tstack.printAll()
# tstack.printPretty()
# b = tstack.both
# print(f"both: {b[0][0]} {b[1][0]}")
# print(f"both: {b[0][1]} {b[1][1]}")
# print(f"both: {b[0][2]} {b[1][2]}")


#<<TODO>> depricated? 
def printRegisters(reglist, regaddrs):
    #print(f"addrs {len(regaddrs)} list {len(reglist)}")
    for i in range (len(regaddrs)):
         print(f"{regaddrs[i]} {reglist[i]}")
    # for i in range (len(regaddrs)):
    #     print(f"regaddrs: {regaddrs[i]}")
    # for i in range (len(reglist)):
    #         print(f"reglist {reglist[i]}")

#gdb command that will print stack registers including certain things from info frame and stat/maps
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
            if(from_tty):
                myProgramStack.printAll()
        else:
            print("not debugging, please run before using.")
        
pstack() 

#gdb command to print all functions. 
class pfunc (gdb.Command):
    """print the functions known to the program at the current point"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pfunc,self).__init__("pfunc",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        argString = arg.strip('').split('-')
        #print(arg)
        print(f"invoking pfunc {arg}")    
        myProgramFunctions.populateFunctions()
        if(from_tty):
            myProgramFunctions.printAll()

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
#we can abuse the vars() function with .get('key') it does not get updated when changed though.
    #thing = vars(myProgram).get('PID')
#<<TODO>> print the top x addresses of stack, maybe i can use this for something else down the road. 
# retheremostcurrent    
class psp (gdb.Command):
    """print the top n addresses of the stack
    if no argument is used, it will print the top 100 addresse """
    #<<TODO>> make color useful and give the user the ability to tweak the number of lines printed 
    def __init__(self):
                                 #cmd user types in goeshere
        super(psp,self).__init__("psp",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking psp") 
        gdb.execute("pprint")
        #gdb.execute('x/10x $sp')
        if(len(arg)>0):
            out = gdb.execute(f'x/{arg}x $sp',to_string = True)
        else:
            out = gdb.execute('x/100x $sp',to_string = True)
        #this is going to be very bad. 
        
        addrs = myProgram.sortedAddrs 
        #print(f"addrs: {addrs}")
        names = myProgram.sortedNames
        #print(f"names: {names}")
        colors = myProgram.sortedColors
        
        #addrs = myProgramStack.stackRegisterAddresses 
        #names = myProgramStack.stackRegisterNames
        #for addr in addrs:
        m2 = out   
        for i in range(len(addrs)): 
            
            #o2 = out.replace()
            try:
                m = re.search(addrs[i],out)
                m2 = re.sub(addrs[i],addrs[i]+"_" +names[i],m2)
                #print(f"{m.group(0)}, {names[i]}")
         #       print(m2)
            except:
                print("exception")
                pass    
        out2 = m2.splitlines()
        const = 35
        printout =""
        count = 0
        for o in out2:
            
            word = o.split()
            #make print output look pretty by messing with space string, and yeah uh ok
           # print(word)
            for i in range(len(word)):
                allout = []
                #fix this better later <<TODO>>
                found = False
                nameSize = len(word[i])
                spaceString = " "
                for j in range(const-(nameSize)):
                    spaceString = spaceString + " "

                for k in range(len(word[i])):
                    #print(word[i][k])
                    if(word[i][k]=='_'):
                        printout = printout + colored(word[i]+spaceString,"red")
                       
                        found = True
                        break
                if(not found):
                    printout = printout + word[i]+spaceString
                    
                #print(f"lenword: {len(word[i])}")
            #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
               
                # if(found):
                #     printout = colored(printout +word[i]+spaceString,"red")
                #     found = False
            print(printout)    
            printout =""
        # for i in range(len(addrs)):
        #     print(addrs, names)
        
        # #o = out.split('\t')
        # o = re.split('\t|\n',out)
        # o2 = []
        # for line in o:
        #     o2.append(line.strip(':'))
        #     print(line)
        # print(o2)
        #print(o)
psp()


#<<rethere>>

class ptest (gdb.Command):
    """used by dev to test single parts of program"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(ptest,self).__init__("ptest",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        myProgramStack.getRegs()
ptest()


class pmode (gdb.Command):
    """prints the current mode of the program"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(pmode,self).__init__("pmode",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        print(f"the current mode is: {myProgram.mode}")
        
pmode()


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
        if(len(arg))<1:
            myProgram.mode = 'default'
            print("changed mode to default")    
        print(f"from_tty: {from_tty}")
        print(f"len arg: {len(arg)} args: {arg}")
        myProgram.mode = arg

changemode()

# class simplepprint (gdb.Command):
#     """user defined gdb command"""
#     def __init__(self):
#                                  #cmd user types in goeshere
#         super(simplepprint,self).__init__("spp",gdb.COMMAND_USER)
#     #this is what happens when they type in the command     
#     def invoke(self, arg, from_tty):
#                 #need flag for all, gui, ...tui?

#         #need add extranious things like data and stuff
#         bigListNames = []
#         bigListAddrs = []
#         bigListColors = []
#         bigListData = []
#         #argString = arg.strip('').split('-')
#         print("invoking pprint")
#         gdb.execute('pfunc')
#         gdb.execute('pvars')
#         gdb.execute('pmap')
#         gdb.execute('pstat')
#         gdb.execute('pstack')
#         myProgramStack.getFrameInfo()
#         print("gathered all data ")
#         #manual stuff 
#         #map 
#         #may need to check if empty here 
#         # if(myProgram.mapHeapBottom==''):
#         #     pass
#         # else:
#         if(myProgram.mapHeapBottom == ""):
#             pass
#         else:
#             bigListNames.append("map_heap_bottom")
#             bigListAddrs.append(myProgram.mapHeapBottom)
#             bigListNames.append("map_heap_top")
#             bigListAddrs.append(myProgram.mapHeapTop)
#             bigListColors.append("white")
#             bigListColors.append("white")

#         bigListNames.append("map_stack_bottom")
#         bigListAddrs.append(myProgram.mapStackBottom)
#         bigListNames.append("map_stack_top")
#         bigListAddrs.append(myProgram.mapStackTop)
#         bigListColors.append("white")
#         bigListColors.append("white")
#         print("finished appending mapstack")
#         #automated stuff 
#         #stack registers
#         #stack registers is not apending the color properly when changing
#         special_registers = ['eip', 'edx', 'edi', 'saved_ebp'] #double check these 
#         for i in range(len(myProgramStack.stackRegisterNames)):
#             bigListNames.append(myProgramStack.stackRegisterNames[i])
#             bigListAddrs.append(myProgramStack.stackRegisterAddresses[i])
#             found = 0
#             for specReg in special_registers:
                
#                 if(myProgramStack.stackRegisterNames[i] == specReg):
#                     bigListColors.append(myProgram.specialRegisterColor)
#                     found = 1
#             if(not found):    
#                 bigListColors.append(myProgram.regColor)
                
#         print("appended stack registers")    

#         #functions
#         for i in range(len(myProgramFunctions.functionsName)):
#             bigListNames.append(myProgramFunctions.functionsName[i])
#             bigListAddrs.append(myProgramFunctions.functionsAddr[i])
#             bigListColors.append(myProgram.funcColor)
#         print("appended functions")        
#         #variable info
#         for i in range(len(myProgramVariables.varNames)):
#             bigListNames.append(myProgramVariables.varNames[i])
#             bigListAddrs.append(myProgramVariables.varAddrs[i])
#             bigListColors.append(myProgram.varColor)
        
#         print("appended big list names, addrs, colors")
#         for name in bigListNames:
#             try:
#                 #variable type with whatis
#                 #out = gdb.execute(f"whatis {var}",to_string = True)
#                 #self.getVariableType()
#                 #print(f"{var}: {out}")
#                 out = gdb.execute(f"print {name}",to_string = True)
#                 o = out.split()
#                 #o = o.replace("'",'')
#                 #print(f"{var}: {out} o:{o} len: {len(o)}")
#                 if(len(o)>3):
#                     #remove ' and " characters
#                     d1 = o[3].strip('\"')
#                     datast =d1.replace("'",'')
#                     print("this is a character")
#                 #   print(print(f"{var}: {o[3][0]}"))
#                 else:
#                     #remove ' and " characters
#                     d1 = o[2].strip('\"')
#                     datast =d1.replace("'",'')
#             #dont add data that has has not been initialized yet. 
#                 print(f"datast: {datast}")
#                 if(datast=='<error:'):
#                    bigListData.append('null')    
#                 #print(f"the datast for {var}: {datast} 0th_char: {datast[0]}")  
#                 else: 
#                     bigListData.append(datast)
#             except gdb.MemoryError:
#                 #print("some memerror, ignoring")
#                 self.varDatas.append('null')
#         
#         print("before printpair")
#         printPair(bigListNames,bigListAddrs,bigListColors,bigListData)
#         print("after printpair")
#         sortedNames, sortedAddrs, sortedColors = sortTheBigList(bigListNames,bigListAddrs,bigListColors)
#         #short message about what color things are 
#         varout = colored("variables "+myProgram.varColor,myProgram.varColor)
#         funcout= colored("functions "+myProgram.funcColor,myProgram.funcColor) 
#         regsout = colored("regs " + myProgram.regColor, myProgram.regColor)
#         specregsout = colored("special registers " + myProgram.specialRegisterColor, myProgram.specialRegisterColor)
#         print(varout,funcout,regsout, specregsout)
#         #now print the full thing 
#         printPair(bigListNames,bigListAddrs,bigListColors,bigListData)
#         #SORTEDDATA GOES HERE
#         myProgram.trackStacks.append([sortedNames, sortedAddrs, sortedColors])
#         # myProgram.everything =  [ [myProgram.programStack.both], 
#         #    [myProgram.programFuncs.funcInfo], [myProgram.programVariables.variableInfo]  ]
#         # count = 0
#         # for e in myProgram.everything:
#         #     print(count,e)
#         #     count +=1
# simplepprint()

#<<TODO>> make saved_EIP point to eip register as data 
class pprint (gdb.Command):
    """run all p commands and hope for the best
    <copy paste information for all functions here>  gdb.execute('pfunc')
    supported commands:
        'pvars'
        prints contents of the stack at the current line in the program. 
            
            Builder mode: 
            simple mode: 
            <complex/full> mode: 
        'pfunc'
            uilder mode: 
            simple mode: 
            <complex/full> mode:
        'pmap'
            uilder mode: 
            simple mode: 
            <complex/full> mode:
        'pstat'
            uilder mode: 
            simple mode: 
            <complex/full> mode:
        'pstack'
            prints contents of the stack at the current line in the program. 
            
            Builder mode: add and print stack 
            simple mode: print most important stack information 
            <complex/full> mode: print all stack information
        'changecolor' type color
            type: var, func, special, regs
                var: changes variable color (default: << color here >>)
                func: changes functions colors (default: << color here >>)
                reg: changes general register colors (default: << color here >>)
                special: changes the special registers colors ('eip', 'edx', 'edi', 'saved_ebp')
            supported colors: https://pypi.org/project/termcolor/

        pprint: print all information and display with the current mode 
            builder mode: 
                print all information that has been "built"
            simple mode: 
                print all simple information
            <complex/full> mode:
                print everything, Yes Everything. You have been warned. 
            <Debug mode>: print debug information (lots of terminal output helpful trace information in finding problems with the program )    
    """
    def __init__(self):
                                 #cmd user types in goeshere
        super(pprint,self).__init__("pprint",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        #need flag for all, gui, ...tui?
        if(myProgram.mode =='complex'):
            builderPrint()
            return
        #need add extranious things like data and stuff
        bigListNames = []
        bigListAddrs = []
        bigListColors = []
        bigListData = []
        #argString = arg.strip('').split('-')
        print("invoking pprint")
        gdb.execute('pfunc')
        gdb.execute('pvars')
        gdb.execute('pmap')
        gdb.execute('pstat')
        gdb.execute('pstack')
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
        print("finished appending mapstack")
        #automated stuff 
        #stack registers
        #stack registers is not apending the color properly when changing
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
                
        print("appended stack registers")    

        #functions
        for i in range(len(myProgramFunctions.functionsName)):
            bigListNames.append(myProgramFunctions.functionsName[i])
            bigListAddrs.append(myProgramFunctions.functionsAddr[i])
            bigListColors.append(myProgram.funcColor)
        print("appended functions")        
        #variable info
        for i in range(len(myProgramVariables.varNames)):
            bigListNames.append(myProgramVariables.varNames[i])
            bigListAddrs.append(myProgramVariables.varAddrs[i])
            bigListColors.append(myProgram.varColor)
             
        #stat 
        if(myProgram.mode != "default"):# or myProgram.mode != "simple"):
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
                        print("eip has been found")
                        break

            if (bigListNames[i] == 'saved_eip'):
                bigListColors[i] = 'magenta' 
                  
                for j in range(len(bigListData)):
                    if(bigListNames[j] == 'eip'):
                        bigListData[i] = 'eip_'+bigListAddrs[j]
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
            printPair(bigListNames,bigListAddrs,bigListColors,bigListData)
        sortedNames, sortedAddrs, sortedColors, sortedData = sortTheBigList(bigListNames,bigListAddrs,bigListColors,bigListData)
        #short message about what color things are 
        varout = colored("variables "+myProgram.varColor,myProgram.varColor)
        funcout= colored("functions "+myProgram.funcColor,myProgram.funcColor) 
        regsout = colored("regs " + myProgram.regColor, myProgram.regColor)
        specregsout = colored("special registers " + myProgram.specialRegisterColor, myProgram.specialRegisterColor)
        stackboundry = colored("stack boundry "+myProgramStack.boundryColor, myProgramStack.boundryColor)
        
        print(varout,funcout,regsout, specregsout, stackboundry)
        #now print the full thing 
        if(from_tty):
            printPair(sortedNames,sortedAddrs,sortedColors,sortedData)
        
        myProgram.sortedAddrs = sortedAddrs
        myProgram.sortedNames = sortedNames
        myProgram.sortedColors = sortedColors
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
            #change to != later <<TODO>>
            if(trackedSet - localSet == set()):
                print("nothing to do here the set is empty")
                #print(trackedSet)
            else:
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

def builderPrint():
    print("builder print")

#modify the printpair cmd to do more than one per columns 
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
def getColor(text):
    #the things we want to highlight
    
    #keyRegs = ['eip', 'saved_eip', 'saved_esp', 'saved_ebp']
    keyRegs = ['eip', 'edx', 'edi', 'saved_ebp, ebp']
    #keyVariables (if first thing is a v``)
    #keyFunction (if first thing is a f)
    #the colors we want to use 
    # keyRegColor = 'red'
    # keyVarColor = 'blue'
    # keyFuncColor = 'green'
    for key in keyRegs:
        if(text == key):
            return 'red'
            #print(key,text[1:])
            
            #textout = colored(text, keyRegColor)
    
    if(text[0]=='r'):
        for key in keyRegs:
            #print(key,text[1:])
            if(text[1:] == key):
            #textout = colored(text, keyRegColor)
                return 'red'
            
        return 'magenta'

    #this is a function
    if(text[0]=='f'):
        #textout = colored(text, keyFuncColor)
        return keyFuncColor
    #this is a variable
    if(text[0]=='v'):
       # textout = colored(text, keyVarColor)
        return keyVarColor
from termcolor import colored

#this method prints things nicely. 
def printPair(names,addrs,colors,data):
    
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

def printPairNoColor(names,addrs,data):
    
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


#debug
# myProgram.programStack.addReg(regaddrs[0],reglist[0])
# myProgramStack.addReg(regaddrs[1],reglist[1])
# print(myProgram.programStack.both)
# print(myProgramStack.both)

#python really doesnt care about variable typing...

# gdb.execute('r')
# myProgramFunctions.populateFunctions()
# print(myProgramFunctions.funcInfo)
# print(myProgramFunctions.functionsAddr)
# print(myProgramFunctions.functionsLine)
# print(myProgramFunctions.functionsName)



"""
get variables by running info locals at 
the beginning of each function (including main)
p variable 
    prints whatever is stored at the variable (garbage before initialized)
p &variable 
    prints the address of this variable

easy path 
break main 
info functions 
set breakpoint for all functions 
r 
info locals (main)
c 
info locals (function)
. . . 
end [Inferior 1 (process <>) exited normally]
r (to restart program and do other things)


we only care about names at first because then gdb will handle the rest
printing a variable not in the current scope ("context")
produces the following error 
No symbol "<variable>" in current context.
so in that case we can just skip it. 
if variable address is not 0 put it in the array 

"""