
class Stack:
    
    stackRegisterAddresses =  []
    stackRegisterNames = []
    both = [stackRegisterAddresses,stackRegisterNames]
    
    dataStart = 0
    dataEnd = 0
    bottomOfStack = "0x00000000"



def addReg(regAddress, regName, stack):
    stack.registerAddresses.append(regAddress)
    stack.registerNames.append(regName)
    sortRegs(stack)

def printRegs(self):
        print(f"{self.registerAddresses} {self.registerNames}")
        print(f"{self.both}")


def sortRegs(self):
    regaddrs = self.registerAddresses 
    reglist = self.registerNames
    
    #dont bother sorting if the length is only 1. 
    #does it even count as an optimization 
    # if its only ever called once?
    if(len(regaddrs)==1):
        pass
    else:
        
        for i in range(len(regaddrs)):
            for j in range(len(regaddrs)):
                # < should be the correct direction
                if int(regaddrs[i],16) < int(regaddrs[j],16):
                # print(f"swapping: {(regaddrs[i])} with {(regaddrs[j])}")
                    tmpaddrs = regaddrs[i]
                    regaddrs[i] = regaddrs[j]
                    regaddrs[j] = tmpaddrs
                    templist = reglist[i]
                    reglist[i] = reglist[j]
                    reglist[j] = templist
