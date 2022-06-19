import gdb
import re 
import os

gdb.execute('b main')
gdb.execute('r')
#get pid here
program = 'simple_program'
regex = f"\d+ pts.0 +..:..:.. {program}"
#get just the pid
regex2 = "\d+ "
out = os.popen('ps').read()
m = re.search(regex,out)
#search the regex of ps for just the PID
m2 = re.search(regex2,m.group(0))

#process id for the program 
procid = m2.group(0)
#strip away those spaces that cause problems in filepaths
procnospace = procid.strip()

useful_stack_info = [23,26,27,28,29,30,45,46,47,48,49,50,51,52]
whatInfo = ["vsize","startcode","endcode", "startStack", "currentESP", "currentEIP", "startData", "endData", "heapExpand", "argStart", "argEnd", "EnvStart", "EnvEnd", "ExitCode"]
info = []
hexinfo = []
command1 = f"cat /proc/{procnospace}/stat | awk "
command2 = "\' {print "
command3 = f"${useful_stack_info[1]}"    
command4 = " } \' "
command_out = command1 + command2 +command3 +command4 
print(command_out)
for location in useful_stack_info:
    command3 = f"${location}" 
    command_out = command1 + command2 +command3 +command4 
    statout = ( (os.popen(f"{command_out}").read()).strip('\n') )
    info.append(statout)
    h = hex(int(statout))
    hexinfo.append(h)
for i in range(len(whatInfo)):
    print(f"{whatInfo[i]} {info[i]} {hexinfo[i]}")
print(f"info: {info}")