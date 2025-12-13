import functions as f
import scipy.sparse as sp
import numpy as np
import matplotlib.pyplot as plt


Lx = Ly = 4          # breytt (var 2)
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 10
m = 10
L = 2               # dæmi 5: afl bara á neðri helming vinstri jaðars
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

vinstriEfri, jLoc0 = f.makePartOfA(*f.vinstriEfri(*breytur), jLoc)
vinstriNedri, jLoc1 = f.makePartOfA(*f.vinstriNedri(*breytur), jLoc0)
nidri, jLoc0       = f.makePartOfA(*f.nidri(*breytur), jLoc1)
uppi, jLoc1        = f.makePartOfA(*f.uppi(*breytur), jLoc0)
haegri, jLoc0      = f.makePartOfA(*f.haegri(*breytur), jLoc1)

megalist = [
    *[x for y in vinstriEfri   for x in y],
    *[x for y in vinstriNedri  for x in y],
    *[x for y in nidri         for x in y],
    *[x for y in uppi          for x in y],
    *[x for y in haegri        for x in y],
    *[x for y in innriPunktar  for x in y]
]

_, vinstriNedriRows, _ = zip(*[x for y in vinstriNedri for x in y])
length = len(list(set(vinstriNedriRows)))

vinstriNedriRows = np.array(list(set(vinstriNedriRows)))
bValues = np.array([-2*P*hx/(L*delta*K) for _ in range(length)])
columns = np.array([0 for _ in range(length)])

b = sp.coo_matrix((bValues, (vinstriNedriRows, columns)), shape=(n*m, 1)).tocsr()

values, rows, cols = map(np.array, zip(*megalist))
A = sp.coo_matrix((values, (rows, cols)), shape=(n*m, n*m)).tocsr()

sol = sp.linalg.spsolve(A, b)

end = time.perf_counter()
print(end-start)

u = np.asarray(sol).reshape((n, m))
T = u + U

x = np.linspace(0, Lx, m)
y = np.linspace(0, Ly, n)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, T)  
ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_zlabel("Temperature (°C)")
plt.show()




