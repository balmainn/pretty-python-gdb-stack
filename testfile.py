import os
import re
import gdb

#eventually give this thing an argument to the program file we are running
#just use PIDOF built in linux thing. come back and fix this later. 
#also can use cat /proc/<PID>/stat | awk '{print $28}' 
#the 28th field of this is the start of the stack.
#problem with awk is it prints it in %lu (long unsingned int format) so we have to convert it anyway


gdb.execute('b main')
gdb.execute('r')
#program we are getting the PID and approximate stack address of
program = 'simple_program'

#regex needed for this to work. 
#get the line containing the pid for our program based on ps
regex = f"\d+ pts.0 +..:..:.. {program}"
#get just the pid
regex2 = "\d+ "
#get the line containing "stack"
stackregex = "\w+-\w+ +\w+-+\w+ \d+ \d+:\d+ \d+ +\[stack]"
#get the max stack address range (because stack randomization is a thing)
stackAddressRegex = "-\w\w\w\w\w\w+"
#use the os to run ps
out = os.popen('ps').read()
#search ps output for line 
m = re.search(regex,out)
#search the regex of ps for just the PID
m2 = re.search(regex2,m.group(0))

#process id for the program 
procid = m2.group(0)
#strip away those spaces that cause problems in filepaths
procnospace = procid.strip()

#print(procnospace)
useful_stack_info = [23,26,27,28,29,30,45,46,47,48,49,50,51,52]
whatInfo = ["vsize","startcode","endcode", "startStack", "currentESP", "currentEIP", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"]
import re
#start location is string[:8]
#end location is string[] 
def getHeapStack(mapString):
    print("~~~~~~~~~~~~")
    heap_stack_regex = ".+\[heap\]|.+\[stack\]"
    arr = mapString.splitlines()
    heapStart = ""
    heapEnd = ""
    stackStart = ""
    stackEnd = ""
    for line in arr:
        m = re.search(heap_stack_regex,line)
        if(type(m) == re.Match):
            print(type(m))
            print(line)
            #avoid problems with grouping nonetype
            try:
                heapOrStack= m.group(0)
                print(f"last chars: {heapOrStack[-3:]}")
                print(f"mgroups0: {m.group(0)}")
                if(heapOrStack[-3:] =="ap]"):
                    #print("this is a heap")
                    heapStart = heapOrStack[:8]
                    heapEnd = heapOrStack[9:18]
                    print(f"heapstart: {heapOrStack[:8]}")
                    print(f"heapend: {heapOrStack[9:18]}")
                else:
                    stackStart = heapOrStack[:8]
                    stackEnd = heapOrStack[9:18]
                    print(f"stack: {heapOrStack[:8]}")
                    print(f"stackend: {heapOrStack[9:18]}")
                    #print("this is a stack")
            #these contain no errors we're looking for    
            except:
                pass
    print(f"heap: {heapStart} to {heapEnd}\nstack: {stackStart} to {stackEnd}")
    return heapStart, heapEnd, stackStart, stackEnd
    
out = os.popen(f'cat /proc/{procnospace}/maps').read()
#print(out)
getHeapStack(out)
gdb.execute('n')
out = os.popen(f'cat /proc/{procnospace}/maps').read()
getHeapStack(out)
#print(out)
gdb.execute('n')
out = os.popen(f'cat /proc/{procnospace}/maps').read()
getHeapStack(out)
#print(out)
# for j in range(5):    

#     out = os.popen(f'cat /proc/{procnospace}/stat').read()
#     #print(out)
#     useful = out.split() 
#     #print(out)
#     #print("OUTPUT FROM C")
#     fromc = os.popen(f'./proctest {procnospace}').read()
#     #print(type(fromc))
#     useful2=fromc.splitlines()
#     #print(type(useful2))
#     #for i in range(len(useful_stack_info)):
#     #    print(f"{useful_stack_info[i]} {whatInfo[i]} {useful2[i]}")
#     print(f"{useful_stack_info[4]} {whatInfo[4]} {useful2[4]}")
#     print(f"{useful_stack_info[5]} {whatInfo[5]} {useful2[5]}")
#     print("~~~~~")

#    gdb.execute('n')    
# for j in useful_stack_info:
#     i = j#-1
#     print(f"#{i} int: {useful[i]} hex: {hex(int(useful[i],16))} len: {len(useful)}")
    #print()
#print(out[i])
#print(type(out))
#gdb.execute('n')


#23 virtual memory size in bytes 
#26 start code 
#    The address above which program text can run.
#(27) endcode  %lu  [PT]
#    The address below which program text can run.

#28 start stack 
#29 current esp value found in kernel stack page 
#30 current EIP (instruction pointer)
#45 start data (address above program uninitialized data is stored)
#46 end data (address below program uninitialized data is stored)
#47 start_brk address above which the program heap can be expanded with
#   (48) arg_start  %lu  (since Linux 3.5)  [PT]
#          Address above which program command-line arguments
#          (argv) are placed.

#   (49) arg_end  %lu  (since Linux 3.5)  [PT]
#          Address below program command-line arguments (argv)
#          are placed.

#   (50) env_start  %lu  (since Linux 3.5)  [PT]
#          Address above which program environment is placed.

#   (51) env_end  %lu  (since Linux 3.5)  [PT]
#          Address below which program environment is placed.

#   (52) exit_code  %d  (since Linux 3.5)  [PT]
#          The thread's exit status in the form reported by
#          waitpid(2).




#reset local variable whenver we continue    
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


# def init_argparse() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser(
#         #usage="%(prog)s [OPTIONS]",
#         description="description goes here"
#     )
#     parser.add_argument(
#         "-f", "--file_path", 
#         help= "specify the file used on gdb"
#     )
#     return parser

# parser = init_argparse()
# args, remaining_args = parser.parse_known_args()

# print(args)
# print(args.file_path[:-2])
# programFilePath = ""
# execPath = ""
# if args.file_path:
#     execPath = args.file_path[:-2]
#     programFilePath = args.file_path
# else:
#     print("nothing to do here")
#     programFilePath = "simple_program.c"
#     execPath = "simple_program"
# print(f"execPath: {execPath}")
# #os.popen(f"gdb ./{execPath} -x pythonexec.py")
# #so as long as you quit out of GDB this works
# out = os.popen(f"gdb ./{execPath} -x pythonexec.py")

# print (out.read())

# out = os.popen('ps').read()
# print(out)
# #program executable name needs inserted below


# #myProgram = Program(PID,execPath,programFilePath)
# myProgram = Program()
# myinit(myProgram,pid=32,ex="ex",fpath="fpath")
# print(myProgram.PID)

# # #myStack = Stack
# # #myProgram = Program(3)
# # #print(myProgram.PID)

# # print("BLAAARAG")
# # funcNames, funcNumbers, funcAddrs = getAllFunctions()
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
