#!/bin/bash
#install dependencies 
sudo apt install python3 pip gcc-multilib 
sudo pip install python-dev-tools termcolor PyQt6 PySide6
#fix PyQt6 because pip install is not enough
sudo python3 -m pip install pip setuptools --upgrade
sudo python3 -m pip install PyQt6
#set .gdbinit in local filepath
echo "set auto-load safe-path /" > .gdbinit
