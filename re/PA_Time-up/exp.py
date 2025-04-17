#!/usr/bin/python
from pwn import *

context.arch = "amd64"
# context.log_level="debug"
r = remote("124.16.75.117", 51008)
r.recvuntil(b"Challenge: ")
line1 = r.recvline(keepends=False)
expression = line1.decode("utf-8")
answer = eval(expression)
print(answer)
# to bytes
answer = str(answer).encode("utf-8")
r.sendline(answer)
r.interactive()


