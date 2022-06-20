#import gdb
import argparse
#oh the jank is bad with this one. 
#everything is a single file now
#but we "should" be able to still import and use things seperately...?
#from stackclass import *
from functions import *
from programclass import *
import os

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        #usage="%(prog)s [OPTIONS]",
        description="description goes here"
    )
    parser.add_argument(
        "-f", "--file_path", 
        help= "specify the file used on gdb"
    )
    return parser

parser = init_argparse()
args, remaining_args = parser.parse_known_args()

print(args)
print(args.file_path[:-2])
programFilePath = ""
execPath = ""
if args.file_path:
    execPath = args.file_path[:-2]
    programFilePath = args.file_path
else:
    print("nothing to do here")
    programFilePath = "simple_program.c"
    execPath = "simple_program"
print(f"execPath: {execPath}")
#os.popen(f"gdb ./{execPath} -x pythonexec.py")
#so as long as you quit out of GDB this works
out = os.popen(f"gdb ./{execPath} -x pythonexec.py")

print (out.read())

out = os.popen('ps').read()
print(out)
#program executable name needs inserted below
c1 = f"ps -C {execPath}"
c2 = "| awk '{print $1}'"
c3 = c1+c2
out = os.popen(f"{c3}").read()
PID = out[3:].strip()

#myProgram = Program(PID,execPath,programFilePath)
myProgram = Program()
myinit(myProgram,pid=32,ex="ex",fpath="fpath")
print(myProgram.PID)

# #myStack = Stack
# #myProgram = Program(3)
# #print(myProgram.PID)

# print("BLAAARAG")
# funcNames, funcNumbers, funcAddrs = getAllFunctions()
# breakAllFunctionsByNumber(funcNumbers)
# gdb.execute('r')
# #main will always be first
# locals = gdb.execute('info locals',to_string=True)
# print(locals)
# gdb.execute('c')
# print("~~~~~~~~~~~")
# #function variables
# locals = gdb.execute('info locals',to_string=True)
# print(locals)
# out = gdb.execute('c',to_string=True)
# print (f"out: {out}")

# easy path 
# info functions 
# set breakpoint for all functions 
# r 
# info locals (main)
# c 
# info locals (function)
# . . . 
# end [Inferior 1 (process <>) exited normally]
# r (to restart program and do other things)







# mystack = stack

# addReg("0xffff0004", "test4", mystack)
# addReg("0xffff0002", "test2", mystack)
# addReg("0xffff0003", "test3", mystack)
# addReg("0xffff0001", "test1", mystack)
# addReg("0xffff0005", "test5", mystack)
# addReg("0xffff0000", "test0", mystack)

# printRegs(mystack)

#this does work but its... wonky 
#o = os.popen('gdb ./simple_program -x hexstuff.py').read()


#sortRegs(mystack)
#printRegs(mystack)
#print(mystack.both)
