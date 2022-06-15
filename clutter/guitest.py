from appJar import gui
import sys
import tkinter as tk

#def click():
#    a = app.getEntry("blarg")
#     print(a)
# app = gui("gui name here", "400x200")
# app.addLabelEntry("blarg")

# app.addButton("button", click)
# app.go()

app=gui("Grid Demo", "720x900")
app.setSticky("news")
app.setExpand("both")
app.setFont(14)
#row, column, col_span, row_span 
def click():
    print ("click")

# app.addLabel("l1", "1", 0, 0,3,3)#, 1, 2) \ncolspan=1\nrowspan=2
# app.addLabel("l2", "2", 0, 3,2,3)#, 2, 2)\ncolspan=2\nrowspan=2"
# app.addTextArea("l3", 4, 0, 5,1,"text")

# app.addButton("b1", click,3,0,1,1)
# app.addButton("b2", click,3,1,1,1)
# app.addButton("b3", click,3,2,1,1)
# app.addButton("b4", click,3,3,1,1)
# app.addButton("b5", click,3,4,1,1)

# app.setLabelBg("l1", "red")
# app.setLabelBg("l2", "blue")
tout = []
filepath = "simple_program.c"
with open(filepath,'r') as f:
    tex = f.readlines()
    for t in tex:
        tout.append(t)

#row, column, col_span, row_span 
app.addTextArea('gdbout',0,0, 6, 3)
app.setTextArea('gdbout', "text",callFunction=True) 
app.addTextArea('code',0,3,6,2)
#bind the enter key to the click function
#might want the ability to find what window is being used. 
#app.bindKey('<return>',click)
app.addButton('b0',click,6,0,0,0)
app.addButton('b1',click,6,1,0,0)
app.addButton('b2',click,6,2,1,1)
app.addButton('b3',click,6,3,1,1)
app.addButton('b4',click,6,4,1,1)
app.addButton('b5',click,6,5,1,1)
app.addTextArea('gdbin',7,0,5,2,text="GDB window")
#runs click function on t2 whenever mouse is put over this (could be useful later)
#maybe use one of these for each window to figure out where the mouse is....?

#app.setTextAreaOverFunction('t2',click)


#runs function click whenver any key is pressed in t2
#app.setTextAreaChangeFunction('t2',click)


#ent = app.getEntryWidget("t1")
#ent.bind("<FocusIn>",click)
#e = app.getEntry('t1')
#e.bindKey("a",click)

#for line in tout:
#    app.addLabel(f"{i}",line)
#    i+=1
app.go()