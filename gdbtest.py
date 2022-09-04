
import gdb
import sys 
print("hello world")
#this is very complicated, will work on this later. 


gdb.execute("file " + sys.argv[1])
type = gdb.Type (sys.argv[0])
print ("sizeof %s = %d" % (sys.argv[0], type.sizeof()))

# def on_stop(p):
#     (status,value) = p.status 
#     if status != gdb.EXIT:
#         gdb.cli()
#     else:
#         sys.exit(value)
# process=gdb.Inferior(sys.argv)
# process.connect("stop", on_stop)
# process.run()





# #tromey.com/blog?p=501
# class SavePrefixCommand (gdb.Command):
#     "prefix command for saving things."

#     def __init__(self):
#         super (SavePrefixCommand, self).__init__
#         ("save", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE,True)
# SavePrefixCommand()

# #from __future__ import with_statement


# class myRunCommand (gdb.Command):
#     """Save the current breakpoints to a file.
# This command takes a single argument, a file name.
# The breakpoints can be restored using the 'source' command."""

#     def __init__ (self):
#         super (myRunCommand, self).__init__ ("save breakpoints",
#                                                        gdb.COMMAND_SUPPORT,
#                                                        gdb.COMPLETE_FILENAME)

#     def invoke (self, arg, from_tty):
#         print("example command myrun")
#         # with open (arg, 'w') as f:
#         #     for bp in gdb.get_breakpoints ():
#         #         print >> f, "break", bp.get_location (),
#         #         if bp.get_thread () is not None:
#         #             print >> f, " thread", bp.get_thread (),
#         #         if bp.get_condition () is not None:
#         #             print >> f, " if", bp.get_condition (),
#         #         print >> f
#         #         if not bp.is_enabled ():
#         #             print >> f, "disable $bpnum"
#         #         # Note: we don't save the ignore count; there doesn't
#         #         # seem to be much point.
#         #         commands = bp.get_commands ()
#         #         if commands is not None:
#         #             print >> f, "commands"
#         #             # Note that COMMANDS has a trailing newline.
#         #             print >> f, commands,
#         #             print >> f, "end"
#         #         print >> f

# myRunCommand ()