from appJar import gui
def click():
    print("click")
app = gui("gui name here", "400x200")
app.addTextArea("blarg")
app.addButton("button", click)
app.go()