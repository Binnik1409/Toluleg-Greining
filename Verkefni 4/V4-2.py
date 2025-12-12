import functions as f
import scipy.sparse.linalg as spla
import numpy as np
import matplotlib.pyplot as plt


Lx = Ly = 2
delta = 0.1
P = 5
L = 2
K = 1.68
H = 0.005

m = n = 10

# A, b = f.build_system(m, n, Lx, Ly, K, H, delta, P, L)
# v = spla.spsolve(A, b)
# U = v.reshape((m, n))
# U = U + 20  # add ambient temperature 20 °C because it assumed 0 °C ambient in the model

# print("Max temperature (°C):", U.max())
# print(f"Temp at center (0,0) (°C): {U[0,0]}")
# print(f"Temp at (0,2) (°C): {U[0,2]}")
# print("Should be ≈ 164.9626 °C")

# X = np.linspace(0, Lx, m)
# Y = np.linspace(0, Ly, n)
# XX, YY = np.meshgrid(X, Y)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(XX, YY, U.T)
# plt.show()

breytur = [n, m, H, K, P, delta, Lx, Ly, L]

A = f.build_system(breytur)
plt.spy(A)
plt.show()