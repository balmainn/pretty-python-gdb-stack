from appJar import gui
def click():
    a = app.getEntry("blarg")
    print(a)
app = gui("gui name here", "400x200")
app.addLabelEntry("blarg")

app.addButton("button", click)
app.go()