#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = process("./games")
r.sendline("guess666")
r.sendline("276951438")
r.sendline(
    "226622222244222222222266668888668888666666886666226666666688668866886622222222222222"
)

r.sendline("across the mountain you see your sincere solution aha123456789ab")
r.interactive()
