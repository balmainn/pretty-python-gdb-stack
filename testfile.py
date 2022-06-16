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
#for j in range(5):
    #for i in useful_stack_info:

for j in range(5):    

    out = os.popen(f'cat /proc/{procnospace}/stat').read()
    #print(out)
    useful = out.split() 
    #print(out)
    #print("OUTPUT FROM C")
    fromc = os.popen(f'./proctest {procnospace}').read()
    #print(type(fromc))
    useful2=fromc.splitlines()
    #print(type(useful2))
    #for i in range(len(useful_stack_info)):
    #    print(f"{useful_stack_info[i]} {whatInfo[i]} {useful2[i]}")
    print(f"{useful_stack_info[4]} {whatInfo[4]} {useful2[4]}")
    print(f"{useful_stack_info[5]} {whatInfo[5]} {useful2[5]}")
    print("~~~~~")

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



