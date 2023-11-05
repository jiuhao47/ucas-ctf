#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 1024

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q
e = 3

pt = bytes_to_long(FLAG)
ct = pow(pt, e, N)

print((N, e))
print(ct)