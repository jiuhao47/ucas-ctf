# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:58:24) 
# [GCC 11.2.0]
# Embedded file name: origincode.py
# Compiled at: 2024-09-14 16:40:52
# Size of source mod 2**32: 1503 bytes
import struct

def shld(a1, a2):
    return (a1 << 1 | a2 >> 31) & 4294967295


def shl(a1):
    return a1 << 1 & 4294967295


def shr(a1):
    return a1 >> 1 & 4294967295


def en(buf):
    for i in range(0, 10, 2):
        ta = buf[i]
        tb = buf[i + 1]
        for k in range(64):
            if tb & 2147483648 == 2147483648:
                tb = shld(tb, ta)
                ta = shl(ta)
                ta = (88777897 ^ ta) & 4294967295
            else:
                tb = shld(tb, ta)
                ta = shl(ta)
        else:
            buf[i] = ta
            buf[i + 1] = tb


def chars_to_int(characters):
    data = (struct.pack)(*('cccc', ), *[char.encode() for char in characters])
    value = struct.unpack(">I", data)[0]
    return value


if __name__ == "__main__":
    res = [
     1314885045, 52669423, 3603395589, 2403896625, 2646202166, 1248852717, 
     3397747772, 555389864, 4216202737, 2381736511]
    print("flag:")
    temp = input()
    if len(temp) == 40:
        reversed_list = []
        for i in range(0, len(temp), 4):
            group = temp[i[:i + 4]]
            reversed_group = group[None[None:-1]]
            reversed_int = chars_to_int(reversed_group)
            reversed_list.append(reversed_int)
        else:
            en(reversed_list)
            for i in range(10):
                if reversed_list[i] != res[i]:
                    print("Wrong")
                    exit(0)
            else:
                print("Correct")
