from sage.all import *
from math import gcd, lcm

with open('enc', 'r') as f:
    exec(f.read())

M = 2**122
k = 8
C = int((2*k**3)**0.5)

L = Matrix(2*k+1, 2*k+1)
for i in range(2*k):
    L[i, i] = 1
    L[i, -1] = C*M**(2*k-i)
L[-1, -1] = -C*N

L = L.LLL()

for v in L:
    v = list(v)
    assert v[-1] % C == 0
    v[-1] //= C

    x = PolynomialRing(ZZ, 'x').gen()

    P = 0
    for i, j in enumerate(v):
        P += abs(j) * x**(2*k-i)

    
    if not P.is_irreducible():
        f =  P.factor()[0][0]
        p = gcd(f(M), N)
        
        assert p != 1 and N % p == 0

        q = N // p
        d = pow(e, -1, lcm(p-1, q-1))
        pt = pow(ct, d, N)
        print(int.to_bytes(pt, pt.bit_length()//8+1, 'big').strip(b'\0'))
        
        break