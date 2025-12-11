import func as f
import scipy.sparse.linalg as spla
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse.linalg as spla


# constants
Lx = Ly = 2
delta = 0.1
P = 5
L = 2
K = 1.68
H = 0.005

m = n = 10

A, b = f.build_system(m, n, Lx, Ly, K, H, delta, P, L)
v = spla.spsolve(A, b)
U = v.reshape((m, n))

print("Max temperature (°C above ambient):", U.max())
print("Should be ≈ 164.9626 °C")  # from PDF

X = np.linspace(0, Lx, m)
Y = np.linspace(0, Ly, n)
XX, YY = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(XX, YY, U.T)
plt.show()
