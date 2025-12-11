import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import func as f

delta = 0.1
m = n = 200
P = 5
K = 1.68
H = 0.005
Lx = Ly = 4
L = 2   # heat applied only over half of height

Ks = np.linspace(1,5,30)
Pmax = []

for Kval in Ks:
    def maxT_P(P):
        A, b = f.build_system(m, n, Lx, Ly, Kval, H, delta, P, L)
        v = spla.spsolve(A, b)
        return v.max() + 20

    low, high = 0, 50
    for _ in range(40):
        mid = 0.5*(low+high)
        if maxT_P(mid) > 100:
            high = mid
        else:
            low = mid

    Pmax.append(mid)

plt.plot(Ks, Pmax)
plt.xlabel("Thermal conductivity K")
plt.ylabel("Max allowed power for T≤100°C")
plt.show()
