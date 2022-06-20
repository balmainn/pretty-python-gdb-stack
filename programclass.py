from stackclass import * 
from heapclass import *

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

"""