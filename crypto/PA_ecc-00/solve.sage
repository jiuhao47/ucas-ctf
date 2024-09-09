'''
print((p, a, b), G)
print(pk)
print(ct)

'''


p = 10829670737591616881
a = 5654694684284925384
b = 8813703413191082292
# 建立椭圆曲线
E = EllipticCurve(GF(p), [a, b])

G = E((1641649954652386070, 6138061874724201376))
pk = E((5002204260689444003, 4864358965035087900))
ct = [E((51088427393127044, 4878776382292322395)), E((10781379197071597919, 6012831518044176787))]
# 计算椭圆曲线的阶
n = E.order()
print(n)
print(G)
print(pk)
# for possible_private_key in range(n):
#     print(possible_private_key)
#     print(G*possible_private_key)
#     if G * possible_private_key == pk:
#         print("Found private key:", possible_private_key)
#         break

# 计算私钥

d = discrete_log(pk,G,operation="+")

print(d)

print(ct[1]-ct[0]*d)

pt = ct[1]-ct[0]*d
print("The FLAG is NeSE{" + str(pt[0]) + str(pt[1]) + "}")

# NeSE{884798257217395294839799228471984755}
