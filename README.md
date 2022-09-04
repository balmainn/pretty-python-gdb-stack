# pretty-python-gdb-stack
takes gdb output of a stack and makes it pretty with python 

# Installation
git clone this repo\
run install.sh 

# Usage 
place pprint.py in the same directory as the executable and .c file that was used to create it.\ 
these files must have the same name, with exception of the extension. Run the below command\
### gdb ./executable -x ppgdb.py
example\
gdb ./simple_program -x ppgdb.py
