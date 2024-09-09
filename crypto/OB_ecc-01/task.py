#!/usr/bin/env sage

from secret import a, b, p
from hashlib import sha256

E = EllipticCurve(GF(p), [a, b])

P = E(68363894779467582714652102427890913001389987838216664654831170787294073636806, 48221249755015813573951848125928690100802610633961853882377560135375755871325)

assert (E(P[0] + 1, P[1]))
assert (E(P[0] + 2, P[1]))

Q = P * 0x1234567890abcdef

# print("The FLAG is NeSE{" + sha256(str(Q[0]).encode()).hexdigest() + "}")
