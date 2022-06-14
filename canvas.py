from appJar import gui

width = 400 
height = 400
num_rectangles = 10
size = 100
app = gui("canvas test", str(width)+'x'+str(height))
canvas = app.addCanvas("c1")
for i in range(num_rectangles):
    #canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_rectangle(((width/2)-size),0,((width/2)+size),i*50)
    canvas.create_text(((width/2)+size)+22, (i*50)-25,text="<--label")
    canvas.create_text(width/2, (i*50)-25,text="address")
#canvas.create_rectangle((width/2)-size,0,(width/2)+size,50)    
app.go()