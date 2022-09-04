import random
from appJar import gui

def getColor():
    r = random.randrange(0,5)
    if r == 0:
        return "red"
    elif r == 1:
        return "blue"
    elif r == 3:
        return "green"
    elif r == 4:
        return "yellow"
lines = []

#with open("gdb.txt"):
gdbfile = open('gdb.txt','r')
all_lines = gdbfile.readlines()    
for line in all_lines:
    lines.append(line)
    #print(line)
print("all lines:")
print(all_lines)
print("array")
print(lines)

gdbfile.close()


app = gui("gui name here", "400x200")
count = 0
for l in lines:
    count_str = str(count)
    app.addLabel(count_str, l)
    app.setLabelBg(count_str,getColor())
    count+=1
# common set functions
#app.setLabelBg("l1", "red")
#app.setLabelBg("l2", "yellow")
#app.setLabelBg("l3", "purple")
#app.setLabelBg("l4", "orange")

app.go()