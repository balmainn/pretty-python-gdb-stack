from appJar import gui

app = gui("gui name here", "400x200")


with open("t.py") as f:
    codetext = f.readlines()
app.addTextArea("codewindow",text=codetext)
app.go()