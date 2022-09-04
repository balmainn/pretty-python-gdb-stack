pointers = "rbp at 0x7fffffffdd40, rip at 0x7fffffffdd48"
pointer = pointers.split()
rbp_comma = pointer[2]
rbp = rbp_comma[:-1]
rip = pointer[5]

print(rbp)
print(rip)

from appJar import gui

def songChanged(rb):
    print(app.getRadioButton(rb))

def reset(btn):
    # set back to the default, but don't call the change function
    app.setRadioButton("song", "Killer Queen", callFunction=False)

app=gui()
app.addRadioButton("song", "Killer Queen")
app.addRadioButton("song", "Paradise City")
app.setRadioButtonChangeFunction("song", songChanged)
app.addButton("Reset", reset)
app.go()