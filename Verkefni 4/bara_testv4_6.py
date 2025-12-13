import functions as f
import scipy.sparse as sp
import numpy as np
import math
import numpy as np
import matplotlib.pyplot as plt

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

results = []

def best_cpu_placement(Lx=10, Ly=10, delta=0.1, P=5, K=1.68, H=0.005, U=20, n=200, m=200):



    for i in range(Lx-1):
        for j in range(i+1, Lx):

            POWER_START = i
            POWER_END = j
            L = j - i
            hot_start = math.ceil(n*POWER_START/Ly)
            hot_end = math.floor(n*POWER_END/Ly)
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

            u = np.asarray(sol).reshape((n, m))

            T = u + U

            results.append((np.mean(T), T, (i, j)))
    return results


Lx = Ly = 10
delta = 0.1
P = 5
K = 1.68
H = 0.005
U = 20
n = 200
m = 200

results = best_cpu_placement(Lx, Ly, delta, P, K, H, U, n, m)
    
best_result = min(results, key=lambda x: x[0])
plt.imshow(best_result[1], origin="lower", extent=[0, Lx, 0, Ly], aspect="auto")
plt.colorbar(label="Temperature (°C)")
plt.xlabel("x (cm)")
plt.ylabel("y (cm)")
plt.show()
print(f'Best power placement: {best_result[2]} with average temperature {best_result[0]} °C')

x = np.linspace(0, Lx, m)
y = np.linspace(0, Ly, n)
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, best_result[1])                     
ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_zlabel("Temperature (°C)")
plt.show()