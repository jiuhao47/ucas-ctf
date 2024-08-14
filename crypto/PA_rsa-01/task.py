#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 512

p = getPrime(BITS)
q = getPrime(BITS)
r = getPrime(BITS)
N_0 = p * r
N_1 = q * r
e = 65537

pt_0 = bytes_to_long(FLAG[:32])
pt_1 = bytes_to_long(FLAG[32:])

ct_0 = pow(pt_0, e, N_0)
ct_1 = pow(pt_1, e, N_1)

print((N_0, e))
print(ct_0)
print((N_1, e))
print(ct_1)
