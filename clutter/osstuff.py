import os
import re
out = os.popen('ps').read()
#\d+ pts.0 +..:..:.. simple_program
print(out)
program = 'python3'
regex = f"\d+ pts.0 +..:..:.. {program}"
regex2 = "\d+ "
m = re.search(regex,out)
#print(type(m.group(0)))
m2 = re.search(regex2,m.group(0))
print(m2.group(0))
#process id for the program 
procid = m2.group(0)
out = os.popen(f"cat /proc/{procid}/maps").read()
print(out)