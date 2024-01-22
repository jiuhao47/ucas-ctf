#!/usr/bin/python
from ctypes import *
from pwn import *

solver = CDLL("./solve.so")
context.arch = "amd64"
r = remote("124.16.75.117", 51002)
r.recvuntil(b"Challenge: ")
line1 = r.recvline(keepends=False)
print(line1)
answer = solver.solve(line1)
print(answer)
r.sendline(str(answer))
r.interactive()
