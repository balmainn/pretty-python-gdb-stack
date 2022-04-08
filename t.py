#gdb -q ./simple_program -x t.py 
import gdb
#from gdb import pretty_printer as pp
from appJar import gui

def breakmain():
    gdb.execute('b main')

def next ():
    pplist = gdb.pretty_printers
    for p in pplist:
        print(p)
    gdb.execute('n')

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
app.addButton("quit", quit)

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