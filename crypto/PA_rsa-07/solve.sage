from Crypto.Util.number import long_to_bytes
from sympy import *
import gmpy2
import libnum

n = 123943239387086699608556204451353950422358520042995929062285651711819368722945482842743120292454469857315179808104100170026907287153397186139773887396847550571191774298514624031671443707772720122423405886861403266724364691156931906983144575779905626126037078474859130261274243771173704229565525845697527966669
e = 48170551200358819369541661989134834938396739922846947971689201878303959028488464802170224222552076130513126537209121971887013188540305465578511378376359995305160384833221577710387796315809399265497700426099285638031179850859159288173922006797415316365326466835295242178663883570908575623699704553952023575171
ct = 30037361833309861562430651164892272803686602192426949114042487401986558960535804013227120250454280166545485884688856701361536238019866928338480797085159409494672997791622233285130801361710522749174415788498978695605243135907455842276596117799537380803270095124708931705790323115118098404087294795411499524201

def transform(x,y):       #使用辗转相处将分数 x/y 转为连分数的形式
    res=[]
    while y:
        res.append(x//y)
        x,y=y,x%y
    return res
    
def continued_fraction(sub_res):
    numerator,denominator=1,0
    for i in sub_res[::-1]:      #从sublist的后面往前循环
        denominator,numerator=numerator,i*numerator+denominator
    return denominator,numerator   #得到渐进分数的分母和分子，并返回

    
#求解每个渐进分数
def sub_fraction(x,y):
    res=transform(x,y)
    res=list(map(continued_fraction,(res[0:i] for i in range(1,len(res)))))  #将连分数的结果逐一截取以求渐进分数
    return res

def get_pq(a,b,c):      #由p+q和pq的值通过维达定理来求解p和q
    par=gmpy2.isqrt(b*b-4*a*c)   #由上述可得，开根号一定是整数，因为有解
    x1,x2=(-b+par)//(2*a),(-b-par)//(2*a)
    return x1,x2

def wienerAttack(e,n):
    for (d,k) in sub_fraction(e,n):  #用一个for循环来注意试探e/n的连续函数的渐进分数，直到找到一个满足条件的渐进分数
        if k==0:                     #可能会出现连分数的第一个为0的情况，排除
            continue
        if (e*d-1)%k!=0:             #ed=1 (mod φ(n)) 因此如果找到了d的话，(ed-1)会整除φ(n),也就是存在k使得(e*d-1)//k=φ(n)
            continue
        
        phi=(e*d-1)//k               #这个结果就是 φ(n)
        px,qy=get_pq(1,n-phi+1,n)
        if px*qy==n:
            p,q=abs(int(px)),abs(int(qy))     #可能会得到两个负数，负负得正未尝不会出现
            d=gmpy2.invert(e,(p-1)*(q-1))     #求ed=1 (mod  φ(n))的结果，也就是e关于 φ(n)的乘法逆元d
            return d
    print("该方法不适用")

t=wienerAttack(e,n)

print(t)

m = pow(ct, t, n)

print(long_to_bytes(m))

# NeSE{an_Example_For_wiener_attack_9asf982u309rudjksfhkjh34h34sdfiusd0fus}
