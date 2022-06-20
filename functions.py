#import gdb
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

