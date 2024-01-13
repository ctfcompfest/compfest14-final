from sage.all import *
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

with open('enc', 'r') as f:
    L = eval(f.readline().strip())
    G = eval(f.readline().strip())
    ctxt = f.readline().strip()

###################################################################

char = GF(2)["x"]("x^69 + x^6 + x^5 + x^2 + 1")
M = companion_matrix(char, format="bottom")

eqs = Matrix(GF(2), [sum((M**(i*69+j))[0] for j in range(69)) for i in range(69)])
res = vector(GF(2), [sum(L[i*69:(i+1)*69]) for i in range(69)])
sol = eqs.solve_right(res)

###################################################################

char= GF(2)["x"]("x^128 + x^29 + x^27 + x^2 + 1")
M = companion_matrix(char, format="bottom")

annihilator = [9, 31, 32, 47]
ones = [i for i, k in enumerate(list(sol)+G) if k]

eqs = Matrix(GF(2), [sum((M**i)[annihilator]) for i in ones])
res = vector(GF(2), [1 for _ in ones])
sol = eqs.solve_right(res)

key = int.to_bytes(int(''.join(map(str, (sol))), 2), 16, 'big')

###################################################################

iv = bytes.fromhex(ctxt[:32])
ctxt = bytes.fromhex(ctxt[32:])
cipher = AES.new(key, 2, iv)
ctxt = unpad(cipher.decrypt(ctxt), 16)
print(ctxt.decode())
