stuff = [["edx","eap","aaa", "bbb"],["0x0000","0xaaaa","0xffff","0xbbbb"],["data", "no data", "blargus","bdata"]]
z = zip(*stuff)
zlist = list(zip(*stuff))
print(zlist)
thing = ["edx","eap","aaa", "bbb"]

a = ["a"]*len(thing)
print(a)