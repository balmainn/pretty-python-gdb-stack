#start conventionalizing
#NAME GOES FIRST THEN ADDRESS 

from inspect import _void
import re 
class Heap:
    heapRegisterAddresses =  []
    heapRegisterNames = []
    heapBoth = [heapRegisterAddresses,heapRegisterNames]

class Stack:
    def __init__(self) -> None:
            
        self.stackRegisterAddresses =  []
        self.stackRegisterNames = []
        self.both = [self.stackRegisterAddresses,self.stackRegisterNames]
        
        self.dataStart = 0
        self.dataEnd = 0
        self.bottomOfStack = "0x00000000"
        
    def addReg(self, regAddress, regName):
        
        self.stackRegisterAddresses.append(regAddress)
        self.stackRegisterNames.append(regName)
        
    
class resource (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("source programclass.py")
resource() 

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
        funcAddrs = self.getFuncAddrs(funcNames)
        print("func addrs: ",funcAddrs)
        return funcNames, funcNumbers, funcAddrs
    def getFuncAddrs(self,funcNames):
        funcAddrs = []
        for name in funcNames:
            out = gdb.execute(f'info address {name}',to_string=True)
        
            m = re.search("0x\d+",out)
            print("Mgroup: ", m.group(0))
            funcAddrs.append(m.group(0))
            print(f"name: {name} out: {out}")
        print("funcaddrs:", funcAddrs)
        return funcAddrs
    def populateFunctions(self):
        self.functionsName, self.functionsLine,  self.functionsAddr = self.getAllFunctions()
        self.funcInfo = [self.functionsName,self.functionsLine,self.functionsAddr]
        print("populated: ", self.functionsName, self.functionsLine,  self.functionsAddr) 
class Program:

    def __init__(self):   
        self.executable =""
        self.filepath = ""
        #PID = getPID()
        self.programStack = Stack()
        self.programHeap = Heap()
        self.programFuncs = Func()
        #arrray of functions... 
        
        self.PID = 0
        self.variableNames = []
        self.variableAddresses = []
        self.variableBoth = [self.variableNames,self.variableAddresses]
        
        self.dataStart = 0
        self.dataEnd = 0
        self.bottomOfStack = "0x00000000"
        #this might be a bad idea...
        #sizes [2], [2], [3], [3]
        self.everything = [ [self.programHeap.heapBoth], [self.programStack.both], [self.programFuncs.functionsAddr], [self.variableBoth]   ]
        print("__init__")
        self.getPID()
        self.getProgramFilePath()
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

class Variable:
    varName = ""
    varData = None
    varAddr = ""

#define like this for ease of use later
myProgram = Program()
myProgramStack = myProgram.programStack
myProgramHeap = myProgram.programHeap
myProgramFunctions = myProgram.programFuncs

gdb.execute('b main')
gdb.execute('r')
registers = gdb.execute('info registers',to_string = True)
regsize = 0
regs = registers.splitlines()
reglist = [] 
regaddrs = []

def printRegisters(regaddrs, reglist):
    for i in range (len(regaddrs)):
        print(f"{regaddrs[i]} {reglist[i]}")

#populate the register list (eip/esp etc.) and regaddrs (0xffff etc.)
for regline in regs:
    line = regline.split()
    name = line[0]
    addr = line[1]
#    print(name, int(addr,16))
    if(int(addr,16)> int("ffff",16)):
#        print(f"{regsize} {line} \n")
        reglist.append(name)
        regaddrs.append(addr)
        regsize = regsize +1
printRegisters(regaddrs,reglist)

def getFrameInfo():
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
    printRegisters(frameRegs,frameRegNames)
    return frameRegs, frameRegNames

myProgram.programStack.addReg(regaddrs[0],reglist[0])
myProgramStack.addReg(regaddrs[1],reglist[1])
print(myProgram.programStack.both)
print(myProgramStack.both)

#python really doesnt care about variable typing...
v = Variable()
v.varAddr = "0xffffcccc"
v.varName = "variable"
v.varData = 3
v.varData = "now i'm a string"
v.varName = 2
print(v.varAddr,v.varName,v.varData)

gdb.execute('r')
myProgramFunctions.populateFunctions()
print(myProgramFunctions.funcInfo)
print(myProgramFunctions.functionsAddr)
print(myProgramFunctions.functionsLine)
print(myProgramFunctions.functionsName)
# for i in range(5):
#     getFrameInfo()
#     gdb.execute('n')
#check the exception
class isGDBRunning (gdb.Command):
    """figure out if gdb is running or not"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(isGDBRunning,self).__init__("amirunning",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        try:
            out =gdb.execute('info registers',to_string=True)
            print( out[-1])
            if out[-1] == 'w':
                print("not running")
            else:
                print("i am running")
        except gdb.error:
            print("some error probably fine")
isGDBRunning()
def isGDBRunningpy():
    out = gdb.execute('info line',to_string=True)
    if (out[0] == 'N'):
        return False
    else:
        return True
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