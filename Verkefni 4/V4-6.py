import functions as f
import scipy.sparse as sp
import numpy as np
import math

def vinstriKalt(n, m, H, K, P, delta, Lx, Ly, L, jStart, jEnd):
    hx = Lx / (m-1)
    
    # jStart = math.floor((L/Ly)*(n-1))+1
    # jEnd = n-1

    iFormula = lambda j: j*m+1
    
    iPlus = [0, 1, 2]

    values = [(2*H*hx/K)-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

def vinstriHeitt(n, m, H, K, P, delta, Lx, Ly, L, jStart, jEnd):
    # jStart = 0
    # jEnd = math.floor((L/Ly)*(n-1))

    iFormula = lambda j: j*m+1

    iPlus = [0, 1, 2]

    values = [-3, 4, -1]

    return jStart, jEnd, iFormula, iPlus, values

Lx = Ly = 10
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 10
m = 10
POWER_START = 2
POWER_END = 8

hot_start = math.ceil(n*POWER_START/Ly)
hot_end = L = math.floor(n*POWER_END/Ly)
hx = Lx/(m-1)

breytur = [n, m, H, K, P, delta, Lx, Ly, L]

import time
start = time.perf_counter()

jLoc_use = 0
innriPunktar = set()
for k in range(1, n-1):   
    inner_row, jLoc = f.makePartOfA(*f.innriRod(*breytur, k), jLoc_use)
    jLoc_use = jLoc
    for x in inner_row:
        innriPunktar.add(x)


vinstriKalt1, jLoc0 = f.makePartOfA(*vinstriKalt(*breytur, 0, hot_start-1), jLoc)
vinstriKalt2, jLoc1 = f.makePartOfA(*vinstriKalt(*breytur, hot_end+1, n-1), jLoc0)
vinstriEfri, jLoc0 = vinstriKalt1.union(vinstriKalt2), jLoc1
vinstriNedri, jLoc1 = f.makePartOfA(*vinstriHeitt(*breytur, hot_start, hot_end), jLoc0)
nidri, jLoc0 = f.makePartOfA(*f.nidri(*breytur), jLoc1)
uppi, jLoc1 = f.makePartOfA(*f.uppi(*breytur), jLoc0)
haegri, jLoc0 = f.makePartOfA(*f.haegri(*breytur), jLoc1)

megalist = [
    *[x for y in vinstriEfri for x in y],
    *[x for y in vinstriNedri for x in y],
    *[x for y in nidri for x in y],
    *[x for y in uppi for x in y],
    *[x for y in haegri for x in y],
    *[x for y in innriPunktar for x in y]
]

_, vinstriNedriRows, _ = zip(*[x for y in vinstriNedri for x in y])
length = len(list(set(vinstriNedriRows)))

vinstriNedriRows = np.array(list(set(vinstriNedriRows)))
bValues = (-2*P*hx/(L*delta*K))*np.ones(length)
columns = np.zeros(length)

b = sp.coo_matrix((bValues, (vinstriNedriRows, columns)), shape=(n*m, 1)).tocsr()

values, rows, cols = map(np.array, zip(*megalist))
A = sp.coo_matrix((values, (rows, cols)), shape=(n*m, n*m)).tocsr()

sol = sp.linalg.spsolve(A, b)

end = time.perf_counter()

print(end-start)


import numpy as np
import matplotlib.pyplot as plt

u = np.asarray(sol).reshape((n, m))

T = u + 20.0                           

plt.imshow(T, origin="lower", extent=[0, Lx, 0, Ly], aspect="auto")
plt.colorbar(label="Temperature (°C)")
plt.xlabel("x (cm)")
plt.ylabel("y (cm)")
plt.show()

# x = np.linspace(0, Lx, m)
# y = np.linspace(0, Ly, n)
# X, Y = np.meshgrid(x, y)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")
# ax.plot_surface(X, Y, T)                     
# ax.set_xlabel("x (cm)")
# ax.set_ylabel("y (cm)")
# ax.set_zlabel("Temperature (°C)")
# plt.show()