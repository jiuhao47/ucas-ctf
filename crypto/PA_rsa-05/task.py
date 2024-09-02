#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 512

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q
e = 65537
d = inverse(e, (p - 1) * (q - 1))
dp = d % (p - 1)

pt = bytes_to_long(FLAG)

ct = pow(pt, e, N)

print((N, e))
print(dp)
print(ct)