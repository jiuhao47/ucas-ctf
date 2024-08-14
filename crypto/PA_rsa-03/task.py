#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 512

def N_gen(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    N = p * q
    return N

e = 3
N_list = [N_gen(BITS) for _ in range(3)]

pt = bytes_to_long(FLAG)
ct_list = [pow(pt, e, N) for N in N_list]

print((N_list, e))
print(ct_list)