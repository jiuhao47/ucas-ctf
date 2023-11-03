#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = process("./games")
r.sendline("guess666")
r.sendline("276951438")
r.interactive()
