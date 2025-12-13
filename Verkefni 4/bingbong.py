import numpy as np


length = 5
n = 2
m = 2
rows = np.zeros((length, n*m))
print(rows)
import scipy.sparse as sp
import numpy as np
import matplotlib.pyplot as plt

def ehhh(n, m, Lx, Ly, Lp=2, H=0.005, K=1.68, d=0.1, P=5):
    hx = Lx / (m - 1)
    hy = Ly / (n - 1)
    Ai = []
    Aj = []
    Agildi = []
    Bi = []
    Bgildi = []
    for k in range(n*m):
        if k % n == 0:
            if (k/n) * hy > Lp:
                Ai += [k]*3
                Aj += [k+2, k+1, k]
                Agildi += [-1, 4, ((2*H*hx)/K)-3]
            else:
                Ai += [k]*3
                Aj += [k, k+1, k+2]
                Agildi += [-3, 4, -1]
                Bi.append(k)
                Bgildi.append((-2*P*hx)/(Lp*d*K))
        elif k % n == n-1:
            Ai += [k]*3
            Aj += [k-2, k-1, k]
            Agildi += [-1, 4, ((2*H*hx)/K)-3]
        elif k // n == 0:
            Ai += [k]*3
            Aj += [k, k+m, k+2*m]
            Agildi += [((2*H*hx)/K)-3, 4, -1]
        elif k // n == n-1:
            Ai += [k]*3
            Aj += [k, k-m, k-2*m]
            Agildi += [((-2*H*hx)/K)-3, 4, -1]
        else:
            Ai += [k]*5
            Aj += [k-m, k-1, k, k+1, k+m]
            Agildi += [hx**2, hy**2, ((2*H*(hx**2)*(hy**2))/(K*d))-4, hy**2, hx**2]
    return Ai, Aj, Agildi, Bi, Bgildi

m = 5
n = 5
Lx = 2
Ly = 2

Ai, Aj, Agildi, bi, bgildi = ehhh(n, m, Lx, Ly)
A = sp.coo_matrix((Agildi,(Ai,Aj)),shape=(n*m,n*m)).tocsr()
bj = np.zeros(len(bi))
b = sp.coo_matrix((bgildi, (bi,bj)),shape=(n*m, 1)).tocsr()

A_solved = sp.linalg.spsolve(A, b)

print(A_solved)
print(b)

# plt.spy(A)
# plt.show()

plt.imshow(A_solved.reshape((n,m)))
plt.show()