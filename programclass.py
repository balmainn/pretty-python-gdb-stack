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


import re
import os



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
   

class Stack:
    def __init__(self) -> None:
            
        self.stackRegisterAddresses =  []
        self.stackRegisterNames = []
        self.both = [self.stackRegisterNames,self.stackRegisterAddresses]
        
        self.dataStart = 0
        self.dataEnd = 0
        self.regColor = 'white'
        self.specialRegColor = 'red'
        #need to do something with this 
        self.bottomOfStack = "0x00000000"
        #we have not added anything to the stack on creation 
        self.stackInit = 0
        # if(len(self.stackRegisterAddresses) == 0):
        #     self.stackInit == 0
        # else:
        #     self.stackInit == 1
    def addReg(self, regName,regAddress):
        
        self.stackRegisterAddresses.append(regAddress)
        self.stackRegisterNames.append(regName)
        self.stackInit = 1
        self.both.clear()
        self.both = [self.stackRegisterNames,self.stackRegisterAddresses]
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
        frameNames, frameRegs = self.getFrameInfo()
        for i in range(len(frameNames)):
            self.addReg(frameNames[i],frameRegs[i])
        #test print
        #print(self.stackRegisterAddresses,self.stackRegisterNames)
        #self.printAll()
        #print("everything added")
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
        arglist = []
        if m:
            #print(m)
            arglist = m[0]
        #print("11-12char: ",frameArr[4][11:12])
        #if the address is unknown, skip it. 
        stored_locals = []
        previous_sp = []
        if frameArr[4][11:12] != 'u':
            m = re.findall(eip_savedEip_regex, frameArr[4]) #,4,6
            stored_locals = m[0]
            previous_sp = m[1]
            print(m)
        #add saved registers to array!
        m = re.findall(eip_savedEip_regex, frameArr[6]) #,4,6
        #print(m)
        m2 = re.findall("e\D\D",frameArr[6])
        #print(m2)
        frameRegs = []
        frameRegNames = []
        for reg in m:
            frameRegs.append(reg)
        for reg in m2:
            frameRegNames.append("saved_frame_"+reg)
        #print(frameRegs, frameRegNames)
        if frame_eip:
            frameRegs.append(frame_eip)
            frameRegNames.append("frame_eip")
        if frame_saved_eip:
            frameRegs.append(frame_saved_eip)
            frameRegNames.append("frame_saved_eip")
        if arglist:
            frameRegs.append(arglist)
            frameRegNames.append("arglist")
        if stored_locals:
            frameRegs.append(stored_locals)
            frameRegNames.append("stored_locals")
        if previous_sp:
            frameRegs.append(previous_sp)
            frameRegNames.append("previous_sp")
        printRegisters(frameRegNames,frameRegs)
        # for i in range(len(frameRegNames)):
        #     print(f"{i} {frameRegNames[i]} {frameRegs[i]}")
        #     self.addReg(frameRegNames[i],frameRegs[i])
        return frameRegNames, frameRegs
    
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
class Func:

    def __init__(self):
        self.functionsName = []
        self.functionsLine = []
        self.functionsAddr = []
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]


    def getAllFunctions(self):
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
        funcAddrs = self.getFuncAddrs(funcNames)
        #print("func addrs: ",funcAddrs)
        return funcNames, funcNumbers, funcAddrs
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
    def populateFunctions(self):
        self.functionsName, self.functionsLine,  self.functionsAddr = self.getAllFunctions()
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]
        #print("populated: ", self.functionsName, self.functionsLine,  self.functionsAddr) 
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

class Program:

    def __init__(self):   
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
        self.executable =""
        self.filepath = ""
        #PID = getPID()
        
        #arrray of functions... 
        
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
        self.getPID()
        self.getProgramFilePath()

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

    def getProgramFilePath(self):
        out = gdb.execute("info line",to_string = True)
        fileregex = "\".+\""
        m = re.search(fileregex,out)
        filename = m.group(0).strip("\"" )
        #print(filename)
        #print(filename[0:-2])
        self.filepath = filename
        self.executable = filename[0:-2]
        
    def getPID(self):
        gdb.execute('b main')
        gdb.execute('r')
        out = gdb.execute('info proc files',to_string = True)
        print(out[8:-1])
        pid = out[8:-1]
        self.PID = pid
    def sortAll(self):
        #sort these methods
        self.everything = [ [self.programHeap.heapBoth], [self.programStack.both], [self.programFuncs.functionsAddr], [self.variableBoth]   ]

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

    def printStatInfo(self):
        for i in range(len(self.statHexInfo)):
            print(f"{i} {self.statWhatInfo[i]} {self.statHexInfo[i]}")

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
        self.varNames = []
        self.varAddrs = []
        self.varDatas = []
        self.variableInfo = [self.varNames,self.varAddrs,self.varDatas]

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
        
    def getVariableType(varstring):
        #if(varString ==)
        pass

    def getLocalVariables(self):
        self.varNames.clear()
        self.varAddrs.clear()
        self.varDatas.clear()
        #variable names are the first grouping of "words" at the beginning 
        out = gdb.execute('info locals', to_string = True)
        localVariableNames = []
        localVarAddresses = []
        variableRegex = "^\w+"
        lines = out.splitlines()
        #variable names
        for line in lines:
        #print(line)
            try:
                m = re.search(variableRegex,line)
            #    print(m.group(0))
                localVariableNames.append(m.group(0))
                self.varNames.append(m.group(0))
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
                #print(f"the datast for {var}: {datast} 0th_char: {datast[0]}")  
                else: 
                    self.varDatas.append(datast)
            except gdb.MemoryError:
                #print("some memerror, ignoring")
                self.varDatas.append('null')
        #dont need to return...?
        return localVariableNames, localVarAddresses

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

    def printAllVars(self):
        allVariableNames = self.varNames
        allVariableAddresses = self.varAddrs
        for i in range(len(allVariableNames)):
            print( allVariableNames[i], allVariableAddresses[i])

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

def printObject(obj):
    obj.printAll()

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

#need to do something with this rethere
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

def isGDBRunningpy():
        pid =  (gdb.selected_inferior().pid)
        if(pid<=0):
            print("i am not running")
            return 0
        else:
            print(f"i am running, my pid is: {pid}")
            return pid


#####~~~~~MAIN~~~~~#####
#define like this for ease of use later
myProgram = Program()
myProgramStack = myProgram.programStack
myProgramHeap = myProgram.programHeap
myProgramFunctions = myProgram.programFuncs
myProgramVariables = myProgram.programVariables

print("welcome to PPGDB")
print("the executable is currently running and a breakpoint has been set in main.")
print("all program modules begin with the letter p.")
print("to see available modules use \"help pprint\"")

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




def printRegisters(regaddrs, reglist):
    for i in range (len(regaddrs)):
        print(f"{regaddrs[i]} {reglist[i]}")

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
class psp (gdb.Command):
    """print the top 10 addresses of the stack"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(psp,self).__init__("psp",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        print("invoking psp") 
        gdb.execute('x/10x $sp')
psp()

#i dont know why there is a difference between what is reported in stat and map
class ptest (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(ptest,self).__init__("ptest",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        if len(arg)>0:
            print(f"arg invoke: {arg}")
        print("invoking ptest") 
        print(f"from_tty: {from_tty}")
        print(f"len arg: {len(arg)}")
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
        bigListColors.append("white")
        bigListColors.append("white")
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
                if(datast=='<error:'):
                   bigListData.append('null') 
                elif(datast=='()}'):
                   bigListData.append('function')       
                #print(f"the datast for {var}: {datast} 0th_char: {datast[0]}")  
                else: 
                    bigListData.append(datast)
            #except gdb.MemoryError or gdb.error:
            except:
                #print("some memerror, ignoring")
                bigListData.append('')
            
        printPair(bigListNames,bigListAddrs,bigListColors,bigListData)
        sortedNames, sortedAddrs, sortedColors, sortedData = sortTheBigList(bigListNames,bigListAddrs,bigListColors,bigListData)
        #short message about what color things are 
        varout = colored("variables "+myProgram.varColor,myProgram.varColor)
        funcout= colored("functions "+myProgram.funcColor,myProgram.funcColor) 
        regsout = colored("regs " + myProgram.regColor, myProgram.regColor)
        specregsout = colored("special registers " + myProgram.specialRegisterColor, myProgram.specialRegisterColor)
        print(varout,funcout,regsout, specregsout)
        #now print the full thing 
        printPair(sortedNames,sortedAddrs,sortedColors,sortedData)
        myProgram.trackStacks.append([sortedNames, sortedAddrs, sortedColors, sortedData])
        # myProgram.everything =  [ [myProgram.programStack.both], 
        #    [myProgram.programFuncs.funcInfo], [myProgram.programVariables.variableInfo]  ]
        # count = 0
        # for e in myProgram.everything:
        #     print(count,e)
        #     count +=1
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
        for stack in s:
            print(f"~~~~stack number {i}~~~~")
            i= i +1
            #printPair(stack[0],stack[1],stack[2])
          
pAllStacks()


def getColor(text):
    #the things we want to highlight
    
    #keyRegs = ['eip', 'saved_eip', 'saved_esp', 'saved_ebp']
    keyRegs = ['eip', 'edx', 'edi', 'saved_ebp']
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
def printPair(names,addrs,colors,data):
    
    const = 20
    print("---------------------------")
    print("reg/var/func/info    address")
    print("---------------------------")
    for i in range(len(names)):
        #print(f"{names[i]}{' '.ljust(10)}{addrs[i]}")
        nameSize = len(names[i])
        spaceString = " "
        for j in range(const-(nameSize)):
            spaceString = spaceString + " "
        if(data == ""):
            out = colored(f"{names[i]}{spaceString}{addrs[i]}",colors[i])
        else:
            out = colored(f"{names[i]}{spaceString}{addrs[i]}     {data[i]}",colors[i])
        print(out)

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