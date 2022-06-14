
from atexit import register
from types import *
from appJar import gui 
import math
import os
import re
import time
#from black import T
import gdb

#look at the following link 
#man7.org/linux/man-pages/man5/proc.5.html
# $26 and 27 for startcode and endcode addresses (these should be static in the program)
def printRegisters(regaddrs, reglist):
    for i in range (len(regaddrs)):
        print(f"{regaddrs[i]} {reglist[i]}")

#eventually give this thing an argument to the program file we are running
#just use PIDOF built in linux thing. come back and fix this later. 
#also can use cat /proc/<PID>/stat | awk '{print $28}' 
#the 28th field of this is the start of the stack.
def getStackAddressEnd():
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
    
    #get stuff from the process map 
    out = os.popen(f"cat /proc/{procnospace}/maps").read()
    #get the line containting [stack]    
    m = re.search(stackregex,out)
    
    #get the approximtae max stack address range
    m2 = re.search(stackAddressRegex,m.group(0))
    #the approximate max stack address. then get rid of the -
    ss= m2.group(0)
    s2 = ss.strip('-')
    #print(s2)
    return int(s2,16)

#returns addrs regslist 
def populateRegisters():
    registers = gdb.execute('info registers',to_string = True)
    regsize = 0
    regs = registers.splitlines()
    reglist = [] 
    regaddrs = []

    #populate the register list (eip/esp etc.) and regaddrs (0xffff etc.)
    for regline in regs:
        line = regline.split()
        print(f"{regsize} {line} \n")
        reglist.append(line[0])
        regaddrs.append(line[1])
        regsize = regsize +1

    stackStart = 0xfffdd000 #(this one is on bottom (i think))
    #stackEnd = 0xffffe000 #(this one is on top) 
    stackEnd = getStackAddressEnd()
    #posative numbers are end - start 
    reglist.append("sp")
    regaddrs.append(hex(stackEnd))
    print(f"{len(regaddrs)} {regsize}")



    done = False
    i = 0
    ilist = []


    #produce a list of indexies the size of our list
    for i in range (regsize):
        if(int(regaddrs[i],16) < 65535): #65535 = ffff
            ilist.append(i)
            

    ilist.sort(reverse=True)

    print(ilist)    
    for i in ilist:
        regaddrs.pop(i)
        reglist.pop(i)

    printRegisters(regaddrs, reglist)

    #bubble sort because why not
    for i in range(len(regaddrs)):
        for j in range(len(regaddrs)):
            if int(regaddrs[i],16) > int(regaddrs[j],16):
            # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                tmpaddrs = regaddrs[i]
                regaddrs[i] = regaddrs[j]
                regaddrs[j] = tmpaddrs
                templist = reglist[i]
                reglist[i] = reglist[j]
                reglist[j] = templist

    print("~~~~~~~~~~~~~~")
    printRegisters(regaddrs, reglist)
    return regaddrs, reglist

    #DEFINE two seperate regions one for stack (around addresses 0x5655 ????)

    #for now though, throw it into an array and put them wherever
#grab the registers from gdb (first you have to set a breakpoint and run)
gdb.execute('b main')
gdb.execute('r')
#app=gui("hex demo", "400x400")
regaddrs0, reglist0 = populateRegisters()
width = 400 
height = 400

num_rectangles = len(regaddrs0)
size = 100
app = gui("canvas test", str(width)+'x'+str(height))
canvas = app.addCanvas("c1")
# i+1 avoides the case where i is 0, thus nothing gets added. 
canvasListTextArr = []
canvasAddressArr = []
for i in range(num_rectangles+8):
    
    #canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_rectangle(((width/2)-size),0,((width/2)+size),(i+1)*50)
    #c1 = canvas.create_text(((width/2)+size)+22, ((i+1)*50)-25,text=f"{reglist0[i]}")
    c1 = canvas.create_text(((width/2)+size)+22, ((i+1)*50)-25,text="BLAAAAANK")
    #c2 = canvas.create_text(width/2, ((i+1)*50)-25,text=f"{regaddrs0[i]}")
    c2 = canvas.create_text(width/2, ((i+1)*50)-25,text="BLAAAANK")
    canvasListTextArr.append(c1)
    canvasAddressArr.append(c2)
#print(canvasListTextArr)
#print(canvasAddressArr)
#canvas.itemconfig(2,text="NEWTEXT")
#app = gui("t2","400x400")
#canvas = app.addCanvas("c2")
def updateText(num_rectangles, canvasAddressArr,canvasListTextArr,regaddrs,reglist):
    for i in range(num_rectangles):
        canvas.itemconfig(canvasAddressArr[i],text=f"{regaddrs[i]}")
        canvas.itemconfig(canvasListTextArr[i],text=f"{reglist[i]}")

def next():
    gdb.execute('n')

def updateRegisters():
    print("update button")
    next()
    print("next")
    regaddrs, reglist = populateRegisters()
    print(regaddrs)
    num_rectangles = len(regaddrs)
    updateText(num_rectangles,canvasAddressArr,canvasListTextArr,regaddrs,reglist)
    

def test():
    print("click")

#app.addButton('updateText',updateText(num_rectangles,canvasAddressArr,canvasListTextArr,regaddrs0,reglist0))
app.addButton('updateRegs',updateRegisters)
app.addButton('t',test)
    #canvas.create_text(((width/2)+size)+22, ((i+1)*50)-25,text=f"{reglist0[i]}")
    #canvas.create_text(width/2, ((i+1)*50)-25,text=f"{regaddrs0[i]}")


app.go()
#app.go()
#gdb.execute('n')
#regaddrs1, reglist1 = populateRegisters()
#gdb.execute('n')
#regaddrs2, reglist2 = populateRegisters()

#for i in range(len(regaddrs0)):
    #print(f"{regaddrs0[i]} {reglist0[i]} || {regaddrs1[i]} {reglist1[i]} || {regaddrs2[i]} {reglist2[i]} ")

# for i in range(len(regaddrs)):
#     #app.addLabel("title","string",row,column)
#     app.addLabel(reglist[i],f"{reglist[i]} {regaddrs[i]}",i,0)

# def clearContents(app,reglist):
#     for i in range(len(reglist)):
#         app.clearLabel(reglist[i])


# app.addButton('clear',clearContents(app,reglist),0,1)    
# #app.addButton('clear',clearContents(app,reglist),len(regaddrs)+1)


# app.go()
