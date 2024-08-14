#!/usr/bin/env python3

from Crypto.Util.number import *

from secret import FLAG

BITS = 1024

p = getPrime(BITS)
q = getPrime(BITS)
N = p * q
# 大数生成
e = 3
# 公钥

pt = bytes_to_long(FLAG)
ct = pow(pt, e, N)

print((N, e))
print(ct)
