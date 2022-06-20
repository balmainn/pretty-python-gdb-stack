#link all files together into a single document

#oh the jank is bad with this one. 
import os
import re
#remove the executable file 
#os.popen('rm -f pythonexec.py')
#os.popen('touch pythonexec.py')
#list of files we want to append
if os.path.exists("pythonexec.py"):
    os.remove("pythonexec.py")

#fileslist = ["heapclass.py","stackclass.py","programclass.py","functions.py","stackmain.py"]
fileslist = ["heapclass.py","stackclass.py","programclass.py","functions.py"]
#fileslist = ["programclass.py","stackmain.py"]
importRegex = "from \w+ import "
lines = []
#read all the information, append to lines
for fi in fileslist:
        with open(f"{fi}",'r') as f:
            line = f.readlines()
            for l in line:
                if ((type(re.search(importRegex,l)) ==re.Match)):
                    pass
                    #print("regexmatch")
                    #print(l)
                else:
                    #print("NO MATCH")
                    #print(l)
                    lines.append(l)
#print(lines)
#         for l in f:
#             #print(l)
#             #print(type(re.search(importRegex,l)))
#             if ((type(re.search(importRegex,l)) !=re.Match)):
#                 lines.append(l)
# #                pass
                #print("line matched, dis bad")

#            else:
#                 lines.append(l)
# #recreate the exectuable file
with open('pythonexec.py','w') as f:
    for line in lines:
        #print(f"writing: {line}")
        f.write(line)
    #f.writelines(lines)
    f.write("gdb.execute('q')")
