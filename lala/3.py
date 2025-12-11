import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
import func as f

# constants
Lx = Ly = 2
delta = 0.1
P = 5
L = 2
K = 1.68
H = 0.005


def solve_maxT(m):
    A, b = f.build_system(m, m, Lx, Ly, K, H, delta, P, L)
    v = spla.spsolve(A, b)
    return v.max()

m_values = [10,20,30,40,50,60,70,80]
ref = solve_maxT(120)   # very fine grid

errors = []
hs = []

for m in m_values:
    Tm = solve_maxT(m)
    hx = Lx/(m-1)
    hs.append(hx)
    errors.append(abs(Tm - ref))

plt.loglog(hs, errors, "o-")
plt.loglog(hs, [errors[0]*(h/hs[0])**2 for h in hs])
plt.xlabel("h")
plt.ylabel("error")
plt.title("Convergence test O(h²)")
plt.show()
