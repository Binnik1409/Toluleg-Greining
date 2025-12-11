import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import func as f

delta = 0.1
P = 5
K = 1.68
H = 0.005
Lx = Ly = 4
L = 2   # heat applied only over half of height

offsets = np.linspace(0, Ly-L, 20)
peakT = []

for off in offsets:
    T = f.solve_with_offset(80, 80, off, L, Lx, Ly, K, H, delta, P)
    peakT.append(T)

best = offsets[np.argmin(peakT)]
print("Best CPU position:", best)
