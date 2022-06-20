class Heap:
    heapRegisterAddresses =  []
    heapRegisterNames = []
    heapBoth = [heapRegisterAddresses,heapRegisterNames]

class Stack:
    
    stackRegisterAddresses =  []
    stackRegisterNames = []
    both = [stackRegisterAddresses,stackRegisterNames]
    
    dataStart = 0
    dataEnd = 0
    bottomOfStack = "0x00000000"



def addReg(regAddress, regName, stack):
    stack.registerAddresses.append(regAddress)
    stack.registerNames.append(regName)
    sortRegs(stack)

def printRegs(self):
        print(f"{self.registerAddresses} {self.registerNames}")
        print(f"{self.both}")


def sortRegs(self):
    regaddrs = self.registerAddresses 
    reglist = self.registerNames
    
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

def getPID() ->int:
        #pid = 3
        return 3

class Program:
    
    executable =""
    filepath = ""
    #PID = getPID()
    programStack = Stack
    programHeap = Heap
    #arrray of functions... 
    programFuncs = []
    PID = 0
    variableNames = []
    variableAddresses = []
    
    dataStart = 0
    dataEnd = 0
    bottomOfStack = "0x00000000"

    def __init__(self):
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

"""#import gdb
import re
def testfunc():
    print("TEST COMPLETE")

def getAllFunctions():
    o = gdb.execute('info functions', to_string = True)
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
    for name in funcNames:
        funcAddrs.append(gdb.execute(f'info address {name}',to_string=True))

    
    return funcNames, funcNumbers, funcAddrs
    
def breakAllFunctionsByName(funcNames):
    for name in funcNames:
        gdb.execute(f'b {name}')

def breakAllFunctionsByNumber(funcNumbers):
    for num in funcNumbers:
        gdb.execute(f'b {num}')


#
#get all of the variables for some list of functions
def getAllVariables(func):
    
    pass

gdb.execute('q')