#!/usr/bin/env python3

from gmpy2 import next_prime
from Crypto.Util.number import *

from secret import FLAG

BITS = 512

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q
NN = int(next_prime(p) * next_prime(q))
e = 65537

pt = bytes_to_long(FLAG)

ct = pow(pt, e, N)

print((N, NN, e))
print(ct)
