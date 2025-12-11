import scipy.sparse as sp
import numpy as np

def ehhh(n, m, hx, hy, L=2, H=0.005, K=1.68, d=0.1, P=5):
    Ai = []
    Aj = []
    Agildi = []
    Bi = []
    Bgildi = []
    for k in range(n*m):
        if k % n == 0:
            if k * hy > L:
                Ai += [k]*3
                Aj += [k+2, k+1, k]
                Agildi += [-1, 4, ((2*H*hx)/K)-3]         
            else:
                Ai += [k]*3
                Aj += [k, k+1, k+2]
                Agildi += [3, -4, 1]
                Bi += [k]
                Bgildi += [(-2*P*hx)/(L*d*K)]
        elif k % n == n-1:
            Ai += [k]*3
            Aj += [k-2, k-1, k]
            Agildi += [-1, 4, ((2*H*hx)/K)-3]
        elif k // n == 0:
            Ai += [k]*3
            Aj += [k, k+m, k+2*m]
            Agildi += [((2*H*hx)/K)-3, 4, -1]
        elif k // n == m-1:
            Ai += [k]*3
            Aj += [k, k-m, k-2*m]
            Agildi += [((-2*H*hx)/K)-3, 4, -1]
        else:
            Ai += [k]*5
            Aj += [k-m, k-1, k, k+1, k+m]
            Agildi += [hx**2, hy**2, ((2*H*(hx**2)*(hy**2))/(K*d))-4, hy**2, hx**2]
    return Ai, Aj, Agildi, Bi, Bgildi

Ai, Aj, Agildi, Bi, Bgildi = ehhh(5, 5, 1, 1)
A = sp.coo_matrix((Agildi,(Ai,Aj)),shape=(5*5,5*5)).tocsr()
print(A.toarray())


