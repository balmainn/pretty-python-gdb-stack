#import gdb
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
    return reglist, regaddrs