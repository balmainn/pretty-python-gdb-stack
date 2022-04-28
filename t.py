#gdb -q ./simple_program -x t.py 
from dis import disassemble
import re
import gdb
#from gdb import pretty_printer as pp
from appJar import gui

def setbreakpoint():
    break_num = app.getEntry("breakpoint")
    gdb.execute("b {break_num}")

def breakfunc():
    gdb.execute('b fuction')

def breakmain():
    gdb.execute('b main')
#retrieve a list of function names and function line numbers. 
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
    breakAllFunctionsByNumber(funcNumbers)
    
def breakAllFunctionsByName(funcNames):
    for name in funcNames:
        gdb.execute(f'b {name}')

def breakAllFunctionsByNumber(funcNumbers):
    for num in funcNumbers:
        gdb.execute(f'b {num}')


def disassemble_main():
    #o = gdb.execute('disassemble main', to_string=True)
    #print(len(o))
    #print(type(o))
    gdb.execute('disassemble main')

def next ():
    o = gdb.execute('n', to_string=True)
    print(f"python: {o}")
    #print(o)

def run():
    gdb.execute('r')

def quit():
    gdb.execute('q')
#gdb.execute('file /bin/cat')
#o = gdb.execute('disassemble exit', to_string=True)
#print(o)
app = gui("gui name here", "400x200")
app.addButton("next", next)
app.addButton("run", run)
app.addButton("break main", breakmain)
app.addButton("break func", breakfunc)
app.addButton("disassemble main", disassemble_main)
app.addButton("get all functions", getAllFunctions)
app.addButton("quit", quit)

#sets a breakpoint
#app.addLabelEntry("breakpoint")
#app.addButton("Set Breakpoint", setbreakpoint)
app.go()

#gdb.execute('quit')


"""
class HelloComman(gdb.Command):
    def __init__(self):
        super(HelloCommand, self).__init__("Hello_world", gdb.COMMAND_NONE)

    dev invoke(self,filename, from_tty):
        #Aquire the GIL
            gdb.execute("call PyGILState_Ensure()")
            #execute the command
            gdb.execute("call PyRun_SimmpleString(\"print(\'hello world\')\")")
            #release the GIL 
            gdb.execute("call PyGILState_Release(\"$1\")")

HelloCommand()
"""

#from pympler import muppy, summary 
#all_objects = muppy.get_objects()
#summ = summary.summarize(all_objects)
#summary.print_(summ)

