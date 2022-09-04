class programStack:
    pass

class Frame:
    pass

#rip return instruction pointer 
#rsp also stack pointer 
#rbp

#rax ?

#eax
#esi
#edi 

#rbp stores original value of RSP resides at posative offsets relative to rbp 
#unixwiz.net/techtips/win32-callconv-asm.html

#esp - stack pointer 
#ebp - base pointer 
#eip - instruction pointer 

#info all-registers 
#info locals -- all local variables of curent stack frame or those that match REG
#info registers 
#info scope?
#info mem - memory region attributes?

#disable ASLR
#echo 0 | sudo tee /proc/sys/kernel/randomize_va_space 
#enable ASLR 
#echo 2 | sudo tee /proc/sys/kernel/randomize_va_space 

#survive reboots 
#kernel.randomize_va_space=0
#  in /etc/sysctl.d/01-disable-aslr.conf 
