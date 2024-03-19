#!/usr/bin/env python3
from pwnlib.util.iters import mbruteforce
from hashlib import sha256
import string
import sys


"""
$ ncat -v [HOST] [PORT]
sha256("KOcNc"+"?") starts with 26bits of zero:
usage: $ python3 solve.py KOcNc
"""

prefixes = sys.argv[1]


def brute(cur):
    content = prefixes + str(cur)
    s = sha256(content.encode())
    if s.hexdigest().startswith("000000") and int(s.hexdigest()[6:8], 16) < 0x40:
        return True
    return False


import pwn

res = mbruteforce(
    brute, string.ascii_lowercase + string.digits, method="upto", length=6, threads=20
)
print(res)
