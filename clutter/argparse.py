import sys 
import os
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--foo', help='foo help')
# args = parser.parse_args()
# print(args)

#args do not work when handeling gdb stuff 

argv = sys.argv
print(argv)
if len(argv) >1:
    for arg in argv:
        print(arg[0:2])
        if arg[0] == 'v' or arg[0:2]=="-v":
            print("entering visual mode")

#needs auto-loading-safe-path to be set in order to work in .gdbinit    
os.popen('gdb ./simple_program ' )
