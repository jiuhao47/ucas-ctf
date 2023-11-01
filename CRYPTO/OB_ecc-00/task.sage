#!/usr/bin/env sage

p = random_prime(2^64)
# 模数p
a = getrandbits(64)
b = getrandbits(64)
# 椭圆曲线参数
E = EllipticCurve(GF(p), [a, b])
# 建立椭圆曲线
G = E.gens()[0]

sk = randrange(0, p)
pk = sk * G

pt = E.random_point()
k = randrange(0, p)

ct = (k * G, pt + k * pk)

print((p, a, b), G)
print(pk)
print(ct)

# print("The FLAG is NeSE{" + str(pt[0]) + str(pt[1]) + "}")
