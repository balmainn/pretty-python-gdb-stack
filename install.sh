#!/bin/bash
#install dependencies 
sudo apt install python3 pip gcc-multilib gdb
sudo pip install python-dev-tools termcolor PyQt6 PySide6
#fix PyQt6 because pip install is not enough

#try installs with pip3 here <<TODO>>


sudo python3 -m pip install pip setuptools --upgrade
sudo python3 -m pip install PyQt6
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

