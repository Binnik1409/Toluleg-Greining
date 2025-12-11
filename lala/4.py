import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import func as f

m = n = 200
Lx = Ly = 2
delta = 0.1
P = 5
L = 2
K = 1.68
H = 0.005



A, b = f.build_system(m, n, Lx, Ly, K, H, delta, P, L)
v = spla.spsolve(A, b)
U = v.reshape((m,n))
print("Max T:", U.max())
