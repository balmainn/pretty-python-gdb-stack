import sys
from termcolor import colored, cprint
#text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])

# print(text)
# class resource (gdb.Command):
#     """reload this file, with changes"""
#     def __init__(self):
#                                  #cmd user types in goeshere
#         super(resource,self).__init__("rs",gdb.COMMAND_USER)
#     #this is what happens when they type in the command     
#     def invoke(self, arg, from_tty):
#         gdb.execute("source syntax.py")
# resource() 


# class test (gdb.Command):
#     """reload this file, with changes"""
#     def __init__(self):
#                                  #cmd user types in goeshere
#         super(test,self).__init__("test",gdb.COMMAND_USER)
#     #this is what happens when they type in the command     
#     def invoke(self, arg, from_tty):
#         print("testing")
#         print("\033[1;32m This text is Bright Green  \n")
# test() 
# #print("\033[1;32m This text is Bright Green  \n")


def getData():
    #for now just gets it as a text file
    #when ready slap the arrays from pprint here
    with open ('output.txt', 'r') as f:
        lines=f.readlines()
    linesarr = []
    for line in lines:        
       # print(line.split())
        linesarr.append(line.split())
   # print(linesarr)
    namesarr =[]
    addrsarr = []
    for i in range(len(linesarr)):
        namesarr.append(linesarr[i][0])
        addrsarr.append(linesarr[i][1])

    #print(namesarr,addrsarr)
    for i in range(len(namesarr)):
        print(f"{namesarr[i]} {addrsarr[i]}")
    return namesarr,addrsarr


def isKeyword(text):
    #the things we want to highlight
    
    #keyRegs = ['eip', 'saved_eip', 'saved_esp', 'saved_ebp']
    keyRegs = ['eip', 'edx', 'edi', 'saved_ebp']
    #keyVariables (if first thing is a v``)
    #keyFunction (if first thing is a f)
    #the colors we want to use 
    keyRegColor = 'red'
    keyVarColor = 'blue'
    keyFuncColor = 'green'
    
    if(text[0]=='r'):
        for key in keyRegs:
            #print(key,text[1:])
            if(text[1:] == key):
            #textout = colored(text, keyRegColor)
                return 'red'
            
        return 'magenta'

    #this is a function
    if(text[0]=='f'):
        #textout = colored(text, keyFuncColor)
        return keyFuncColor
    #this is a variable
    if(text[0]=='v'):
       # textout = colored(text, keyVarColor)
        return keyVarColor

names, addrs = getData()

for i in range(len(names)):
    color = isKeyword(names[i])
    out = colored(f'{names[i][0]}    {names[i][1:]} {addrs[i]}',color)
    print(out)