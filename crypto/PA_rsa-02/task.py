#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 512

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q
e_0 = 1337
e_1 = 7331

pt = bytes_to_long(FLAG)

ct_0 = pow(pt, e_0, N)
ct_1 = pow(pt, e_1, N)

print((N, e_0, e_1))
print(ct_0)
print(ct_1)
