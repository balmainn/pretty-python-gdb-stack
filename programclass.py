from stackclass import * 
from heapclass import *

def getPID() ->int:
        #pid = 3
        return 3

class Program:
    
    executable =""
    filepath = ""
    #PID = getPID()
    programStack = Stack
    programHeap = Heap
    PID = 0
    
    def __init__(self, pid):
      self.PID = pid
