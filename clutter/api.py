import gdb.printing

print("hello world")


#tromey.com/blog?p=501
class SavePrefixCommand (gdb.Command):
    "prefix command for saving things."

    def __init__(self):
        super (SavePrefixCommand, self).__init__
        ("save", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE,True)
    SavePrefixCommand()