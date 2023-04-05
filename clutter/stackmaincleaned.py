#import gdb
#import argparse
#oh the jank is bad with this one. 
#everything is a single file now
#but we "should" be able to still import and use things seperately...?
#from stackclass import *
#from functions import *
#from programclass import *
import os
import gdb 
import re
from functions import *

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
# gdb.execute('b main')
# gdb.execute('r')
# programExec = "simple_program"


def printPair(names,addrs):
    for i in range(len(names)):
        print(f"{names[i]} {addrs[i]}")