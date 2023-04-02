#!/bin/bash
#install dependencies 
apt update
apt install python3 pip gcc-multilib gdb -y
pip install python-dev-tools pygments termcolor 


python3 -m pip install pip setuptools --upgrade

#set safe auto load in local .gdbinit
echo "set auto-load safe-path /" > .gdbinit
#set safe auto load globally (make sure gdb directory exists first)
cd ~
if [ -d ~/.config/gdb/ ]
then
    echo "set auto-load safe-path /" > ~/.config/gdb/.gdbinit
else 
    cd ~/.config/
    mkdir gdb && cd gdb
    echo "set auto-load safe-path /" > .gdbinit
fi

