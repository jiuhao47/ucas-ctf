#!/usr/bin/env python3

import random
from Crypto.Util.number import *

from secret import FLAG

BITS = 512

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q

while True:
    d = random.randrange(1, 2**266)
    e = inverse(d, (p - 1) * (q - 1))
    if (e * d) % ((p - 1) * (q - 1)) == 1:
        break

pt = bytes_to_long(FLAG)

ct = pow(pt, e, N)

print((N, e))
print(ct)
