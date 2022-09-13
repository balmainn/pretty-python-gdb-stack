# pretty-python-gdb-stack
Currently in Alpha Version. 
takes gdb output of a stack and makes it pretty with python 

# Installation
git clone this repo\
run install.sh 

# Using 
place pprint.py in the same directory as the executable and .c file that was used to create it. 
these files must have the same name, with exception of the extension. Run the below command
### gdb ./executable -x ppgdb.py
example\
gdb ./simple_program -x ppgdb.py

if gdb complains about auto-load safe-path not being enabled, add the following line to  your .gdbinit file. this file could be located in ~/.config/gdb/.gdbinit
set auto-load safe-path /

# Commands
'pwindow'
 - Opens the gui. The gui supports the following typed commands as well as any gdb command. 

'pvars'
- Prints variables, their contents, and location on the stack

'pfunc'

- Prints functions and their location on the stack

'pmap'

- Prints information from /proc/$PID/maps

'pstat'

- Prints information from /proc/$PID/stat

'pstack'

- prints contents of the stack at the current line in the program.

'pprint'

- print all stack information and display with the current mode

'pauto'

Prints stack information for each line in the code reachable by gdb "n"

displays this information in the created file "all_stacks.txt"

'pas'

- print all stacks
-- print stack information for each time pprint was called.

## modes of operation

default mode:
- print all simple information. certain information from /proc/$pid/stat and /maps has been left out for simplicity.

complex mode:
- print everything, Including the information left out of the default mode.

Debug mode: 
- print debug information (lots of terminal output helpful trace information in finding problems with the program )
- enabled by changing DEBUG = 1 at the top of the pprint.py file. 