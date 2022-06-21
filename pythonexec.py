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
    
def getFuncAddrs(funcNames):
    funcAddrs = []
    for name in funcNames:
        funcAddrs.append(gdb.execute(f'info address {name}',to_string=True))
    return funcAddrs

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
    funcAddrs = getFuncAddrs(funcNames)

    return funcNames, funcNumbers, funcAddrs
    
def breakAllFunctionsByName(funcNames):
    for name in funcNames:
        gdb.execute(f'b {name}')


def getThingsFromStat(process):
    procnospace = getProcessPID(process)
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
    
    #for i in range(len(whatInfo)):
        #print(f"{whatInfo[i]} {info[i]} {hexinfo[i]}")
    
    return whatInfo, hexinfo
    #print(f"info: {info}")


#get the stack and the heap approximate locations
#from /proc/<pid/maps
#input is this file as a string (os.popen(...).read())
def getProcessPID(process):
    c1 = f"ps -C {process}"
    c2 = "| awk '{print $1}'"
    c3 = c1+c2
    out = os.popen(f"{c3}").read()
    PID = out[3:].strip()
    return PID

def getHeapStack(process):
    PID = getProcessPID(process)
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
                    heapStart = heapOrStack[:8]
                    heapEnd = heapOrStack[9:18]
                #    print(f"heapstart: {heapOrStack[:8]}")
                #    print(f"heapend: {heapOrStack[9:18]}")
                else:
                    stackStart = heapOrStack[:8]
                    stackEnd = heapOrStack[9:18]
                #    print(f"stack: {heapOrStack[:8]}")
                #    print(f"stackend: {heapOrStack[9:18]}")
                    #print("this is a stack")
            #these contain no errors we're looking for    
            except:
                pass
    print(f"heap: {heapStart} to {heapEnd}\nstack: {stackStart} to {stackEnd}")
    return heapStart, heapEnd, stackStart, stackEnd

def printRegisters(regaddrs, reglist):
    for i in range (len(regaddrs)):
        print(f"{regaddrs[i]} {reglist[i]}")

#returns addrs regslist 
def populateRegisters():
    #print("POPULATE REGISTESR")
    registers = gdb.execute('info registers',to_string = True)
    regsize = 0
    regs = registers.splitlines()
    reglist = [] 
    regaddrs = []

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
    #print("at the end")
    #print(reglist)
    #print(regaddrs)
        
    return reglist, regaddrs 

def updateRegisters():
    print("update button")
    next()
    print("next")
    regaddrs, reglist = populateRegisters()
    print(regaddrs)
    #num_rectangles = len(regaddrs)
    #updateText(num_rectangles,canvasAddressArr,canvasListTextArr,regaddrs,reglist)
    
def sortRegisters(reglist,regaddrs):
    i = 0 
    ilist = []

    #produce a list of indexies the size of our list
    for i in range (len(regaddrs)):
        #this if is probably redundant
        if(int(regaddrs[i],16) < 65535): #65535 = ffff
            ilist.append(i)
            

    ilist.sort(reverse=True)

    print(ilist)    
    for i in ilist:
        regaddrs.pop(i)
        reglist.pop(i)

    printRegisters(regaddrs, reglist)

    #bubble sort because why not
    
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

    print("~~~~~~~~~~~~~~")
    printRegisters(regaddrs, reglist)
    return reglist, regaddrs#import gdb
#import argparse
#oh the jank is bad with this one. 
#everything is a single file now
#but we "should" be able to still import and use things seperately...?
import os
import gdb 
import re

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
    for name in funcNames:
        funcAddrRe= "0x\w+"
        out = gdb.execute(f'p &{name}',to_string=True).splitlines()
        for line in out:
            m = re.search(funcAddrRe,line)
            try:
                addr = m.group(0)
                funcAddrs.append(addr)
            except:
                pass        
        #funcAddrs.append(gdb.execute(f'info address {name}',to_string=True))
    return funcNames, funcNumbers, funcAddrs


def breakAllFunctionsByNumber(funcNumbers):
    for num in funcNumbers:
        gdb.execute(f'b {num}')
    



def getLocalVariables():
    #variable names are the first grouping of "words" at the beginning 
    out = gdb.execute('info locals', to_string = True)
    localVariableNames = []
    localVarAddresses = []
    variableRegex = "^\w+"
    lines = out.splitlines()

    for line in lines:
    #print(line)
        try:
            m = re.search(variableRegex,line)
            #print(m.group(0))
            localVariableNames.append(m.group(0))
        except:
            pass
        #print(variableNames)


    for var in localVariableNames:
        out = gdb.execute(f"print &{var}",to_string = True)
        #print(out)
        #this may need to be shortened.
        v = out[-11:].strip()
        #print(f"v {v}")
        localVarAddresses.append(v)

    return localVariableNames, localVarAddresses

def gatherAllVariables():
    
    allVariableNames = []
    allVariableAddresses = []

        #for each function get its variables
    for i in range(len(funcNames)):
        try:
            localVariableNames = []
            localVarAddresses = []
            localVariableNames, localVarAddresses = getLocalVariables()
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

def printAllVars(): 
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

def sortTheBigList(regaddrs,reglist):
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
    return reglist, regaddrs

#~~~~~~~~MAIN~~~~~~~~~~~~#
gdb.execute('b main')
gdb.execute('r')
programExec = "simple_program"
#firstTimeExecution()
#def firstTimeExecution():
PID = getProcessPID(programExec)
funcNames, funcNumbers, funcAddrs = getAllFunctions()
breakAllFunctionsByNumber(funcNumbers)

#update variable location 
#it is important to always run after gathering all variables
allVariableNames, allVariableAddresses = gatherAllVariables()
gdb.execute('r')

statTextInfo, statHexInfo = getThingsFromStat(programExec)
addStatText= []
addStatHex = []

#need to tweak the things i populate later
for i in range(len(statHexInfo)):
  #  print(int(statHexInfo[i],16))
    #if address < FFFF we dont care to display it
    #if(int(statHexInfo[i],16) >=65535):
    if(int(statHexInfo[i],16) >=int("FFFFFF",16)):
        addStatText.append(statTextInfo[i])
        addStatHex.append(statHexInfo[i])

reglist, regaddrs = populateRegisters()
#printRegisters(regaddrs,reglist)
#sorting does not work 
li,ad =sortRegisters(reglist,regaddrs)
#printRegisters(ad,li)

heapStart, heapEnd, stackStart, stackEnd = getHeapStack(programExec)
allVariableNames, allVariableAddresses = updateVariables(allVariableNames,allVariableAddresses)

def printPair(names,addrs):
    for i in range(len(names)):
        print(f"{names[i]} {addrs[i]}")

#print(statTextInfo)
#print(addStatText)

#general update sequence 
for i in range(5):
    bigListNames = []
    bigListNames.append("heapStart")
    bigListNames.append("heapEnd")
    bigListNames.append("stackStart")
    bigListNames.append("stackEnd")

    bigListAddrs = []
    try:
        #location of the heap
        heapStart, heapEnd, stackStart, stackEnd = getHeapStack(programExec)
        bigListAddrs.append(heapStart)
        bigListAddrs.append(heapEnd)
        bigListAddrs.append(stackStart)
        bigListAddrs.append(stackEnd)
        #function addresses needs updating for sure
        # funcAddrs = getFuncAddrs(funcNames)
        # for i in range(len(funcNames)):
        #     bigListNames.append(funcNames[i])
        #     bigListAddrs.append(funcAddrs[i])
        #variables 
        varNames, varAddrs = updateVariables(allVariableNames,allVariableAddresses)
        for i in range(len(varNames)):
            bigListNames.append(varNames[i])
            bigListAddrs.append(varAddrs[i])
        #registers
        reglist, regaddrs = populateRegisters()
        for i in range(len(varNames)):
            bigListNames.append(reglist[i])
            bigListAddrs.append(regaddrs[i])
        statTextInfo, statHexInfo = getThingsFromStat(programExec)
        for i in range(len(statTextInfo)):
            bigListNames.append(statTextInfo[i])
            bigListAddrs.append(statHexInfo[i])
        gdb.execute('n')
        print("~~~~~~~~THE BIG PRINT1~~~~~~~~``")
        sortedNames,sortedAddrs = sortTheBigList(bigListAddrs,bigListNames)
        printPair(sortedNames,sortedAddrs)
    except:
        pass
    
    #printPair(bigListNames,bigListAddrs)

#     print("~~~~heapstack~~~")
#     print(heapStart, heapEnd, stackStart, stackEnd)
#     updateVariables()
#     printAllVars()
#    gdb.execute('n')

    #localVarAddresses.append(v)
  
#gdb.execute('c')
#getLocalVariables()
gdb.execute('q')