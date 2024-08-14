#!/usr/bin/env sage

p = random_prime(2^64)
# 模数p
a = getrandbits(64)
b = getrandbits(64)
# 椭圆曲线参数
E = EllipticCurve(GF(p), [a, b])
# 建立椭圆曲线
G = E.gens()[0]
# 选择一点作为生成元

sk = randrange(0, p)
# 私钥
pk = sk * G
# 公钥

pt = E.random_point()
# 明文
k = randrange(0, p)

ct = (k * G, pt + k * pk)
# 密文

print((p, a, b), G)
print(pk)
print(ct)
# 打印密文

# print("The FLAG is NeSE{" + str(pt[0]) + str(pt[1]) + "}")
# 解密过程
# m=pt+k*pk-(k*G/G)*pk