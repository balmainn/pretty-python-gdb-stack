#from stackclass import * 
#from heapclass import *
import re 
class resource (gdb.Command):
    """user defined gdb command"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        gdb.execute("source programclass.py")
resource() 

class Program:

    def __init__(self):   
        self.executable =""
        self.filepath = ""
        #PID = getPID()
       # self.programStack = Stack
        #self.programHeap = Heap
        #arrray of functions... 
        self.programFuncs = []
        self.PID = 0
        self.variableNames = []
        self.variableAddresses = []
        
        self.dataStart = 0
        self.dataEnd = 0
        self.bottomOfStack = "0x00000000"
        print("__init__")

def myinit(program,pid,ex,fpath):
    program.PID = pid
    program.executable = ex
    program.filepath = fpath
class func:
    functionsName = []
    functionsLine = []
    functionsAddr = []
    funcInfo = [functionsName,functionsLine,functionsAddr]

def getVariables():
    pass




p = Program()
print(p.PID)
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
    #get names with e\D\D
    #frame_stack_eip 
    # for i in range(len(frameArr)):
    #     print(i, frameArr[i])
    
    #make these lables frame_regName

for i in range(5):
    getFrameInfo()
    gdb.execute('n')

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