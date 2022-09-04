import re
registersString = """eax            0xf7fb6088          -134520696
ecx            0x9321354d          -1826540211
edx            0xffffce64          -12700
ebx            0x0                 0
esp            0xffffce3c          0xffffce3c
ebp            0x0                 0x0
esi            0xf7fb4000          -134529024
edi            0xf7fb4000          -134529024
eip            0x56556289          0x56556289 <main>
eflags         0x246               [ PF ZF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99"""

regexAll = "\b\S*\b"
registerInfo = registersString.splitlines()
for r in registerInfo:
     thing = re.search(regexAll,r).group()
     print(thing)

#name is this regex ^\S*
#contents is htis regex \S*$ 
