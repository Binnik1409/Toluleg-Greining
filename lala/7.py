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

target = 100
low, high = 0, 50

for _ in range(40):
    mid = 0.5*(low+high)
    if f.maxT_for_power(mid, m, n, Lx, Ly, K, H, delta, L) > target:
        high = mid
    else:
        low = mid

print("Max allowed power P =", mid)
