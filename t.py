# #gdb -q ./simple_program -x t.py 

# import gdb
# #from gdb import pretty_printer as pp

# def get_rbp_and_rip():
#     pointers = gdb.execute("info frame")
#     pointer = pointers.s

# def setbreakpoint():
#     break_num = app.getEntry("breakpoint")
#     gdb.execute("b {break_num}")

# def breakmain():
#     gdb.execute('b main')

# def disassemble_main():
#     o = gdb.execute('disassemble main', to_string=True)
#     print(len(o))
# def next ():
#     o = gdb.execute('n', to_string=True)
#     print(f"python: {o}")
#     #print(o)



# def run():
#     gdb.execute('r')

# def quit():
#     gdb.execute('q')
# #gdb.execute('file /bin/cat')
# #o = gdb.execute('disassemble exit', to_string=True)
# # #print(o)
# # app = gui("gui name here", "400x200")
# # app.addButton("next", next)
# # app.addButton("run", run)
# # app.addButton("break main", breakmain)
# # app.addButton("disassemble main", disassemble_main)
# # app.addButton("quit", quit)
# # info = ""
# # app.addTextArea(info)
# # #sets a breakpoint
# # #app.addLabelEntry("breakpoint")
# # #app.addButton("Set Breakpoint", setbreakpoint)
# # app.go()

# #gdb.execute('quit')


# """
# class HelloComman(gdb.Command):
#     def __init__(self):
#         super(HelloCommand, self).__init__("Hello_world", gdb.COMMAND_NONE)

#     dev invoke(self,filename, from_tty):
#         #Aquire the GIL
#             gdb.execute("call PyGILState_Ensure()")
#             #execute the command
#             gdb.execute("call PyRun_SimmpleString(\"print(\'hello world\')\")")
#             #release the GIL 
#             gdb.execute("call PyGILState_Release(\"$1\")")

# HelloCommand()
# """

# #from pympler import muppy, summary 
# #all_objects = muppy.get_objects()
# #summ = summary.summarize(all_objects)
# #summary.print_(summ)


class resource (gdb.Command):
    """reload this file, with changes"""
    def __init__(self):
                                 #cmd user types in goeshere
        super(resource,self).__init__("rs",gdb.COMMAND_USER)
    #this is what happens when they type in the command     
    def invoke(self, arg, from_tty):
        
        #gdb.execute("source test.py")
        print("test print completed")
resource() 