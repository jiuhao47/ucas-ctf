from Crypto.Util.number import long_to_bytes

N = [
    81923544864021241359127196669433067656312206725026182841046033151509784125115526074250159776536326062877116770043239171448803000700987193478063352956407226330595889756983060923395164289995609449997370160554182033406727778287676155685508215655056238212498741386688437056735385578005273448778940883826082380001,
    81923544864021241359127196669433067656312206725026182841046033151509784125115526074250159776536326062877116770043239171448803000700987193478063352956409592960587608497671236774918268748511801075731846134465649218132151284428289214624285960174182094255406384884700031319340073827244700965629213796821513047989,
]

ct = 15677341500708390774457921589635744675447490572890192121159639549238703015865287789600789651972557347554170748028258840887962228204267238248315281233939105341528609760455645559240760189756704766849217457247435716776492204585077413166730971399630840228012438843253781267491033191599840786854118240763137564715
e = 65537
# N=N[0] NN=N[1]

print(floor(sqrt(N[0])))
N_sqrt = floor(sqrt(N[0]))
print(floor(sqrt(N[1])))
NN_sqrt = floor(sqrt(N[1]))


def fermat_factorization(n):
    factor_list = []
    a = floor(sqrt(n))
    while True:
        a += 1
        b2 = a * a - n
        if b2.is_square():
            b = floor(sqrt(b2))
            factor_list.append([a + b, a - b])
            if len(factor_list) == 2:
                break
    return factor_list


n = N[0] * N[1]

factor_list = fermat_factorization(n)

print(factor_list)

X1, Y1 = factor_list[0]
X2, Y2 = factor_list[1]
assert X1 * Y1 == n
assert X2 * Y2 == n
p = gcd(X1, X2)
q = X1 // p
p1 = gcd(Y1, Y2)
q1 = Y1 // p1
print("p=", p)
print("q=", q)
print("p1=", p1)
print("q1=", q1)

phi = (p1 - 1) * (q - 1)

d = inverse_mod(e, phi)

m = pow(ct, d, N[0])


print(long_to_bytes(m))

# NeSE{N_can_be_fact0red_giv3n_N_and_NN_dsf79y3r9822983h2893r29}