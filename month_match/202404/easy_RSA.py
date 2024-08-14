
import libnum

p=libnum.generate_prime(1024)
q=libnum.generate_prime(1024)
e1=2333
e2=23333
m=FLAG
m=libnum.s2n(m)
n=p*q

c1=pow(m,e1,n)
c2=pow(m,e2,n)
print("n1:",n)
print("e1:",e1)
print("c1:",c1)
print("n2:",n)
print("e2:",e2)
print("c2:",c2)

