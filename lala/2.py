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

A, B = f.heatsink_fd(Lx, Ly, delta, H, K, P, m, n, L)
u = spla.spsolve(A, B)

U = u.reshape((n, m))
print("Temperature at each grid point (°C):")
print(U)
print(f"Max temperature: {np.max(U):.2f} °C")
print(f"Min temperature: {np.min(U):.2f} °C")

